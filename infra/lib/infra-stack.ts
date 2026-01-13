import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecr_assets from 'aws-cdk-lib/aws-ecr-assets';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as cloudfront_origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as appscaling from 'aws-cdk-lib/aws-applicationautoscaling';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ========================================
    // VPC
    // ========================================
    const vpc = new ec2.Vpc(this, 'ResilioVpc', {
      maxAzs: 2,
      natGateways: 2, // One per AZ for high availability
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 24,
          name: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
        },
      ],
    });

    // ========================================
    // Secrets
    // ========================================
    const djangoSecret = new secretsmanager.Secret(this, 'DjangoSecret', {
      secretName: 'resilio/django',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({ username: 'admin' }),
        generateStringKey: 'secret_key',
        excludePunctuation: true,
        passwordLength: 50,
      },
    });

    // S3 Upload Credentials Secret
    // This secret needs to be manually populated with AWS credentials that have S3 access
    // After deployment, update the secret with:
    // aws secretsmanager put-secret-value --secret-id resilio/s3-upload --secret-string '{"access_key_id":"YOUR_KEY","secret_access_key":"YOUR_SECRET"}'
    const s3UploadSecret = new secretsmanager.Secret(this, 'S3UploadSecret', {
      secretName: 'resilio/s3-upload',
      description: 'AWS credentials for S3 file uploads to dub01hackathongoal bucket',
      secretObjectValue: {
        access_key_id: cdk.SecretValue.unsafePlainText('PLACEHOLDER_UPDATE_AFTER_DEPLOY'),
        secret_access_key: cdk.SecretValue.unsafePlainText('PLACEHOLDER_UPDATE_AFTER_DEPLOY'),
      },
    });

    // Reference the existing S3 bucket for uploads
    const uploadBucket = s3.Bucket.fromBucketName(this, 'UploadBucket', 'dub01hackathongoal');

    // ========================================
    // RDS PostgreSQL Database
    // ========================================
    const dbSecurityGroup = new ec2.SecurityGroup(this, 'DbSecurityGroup', {
      vpc,
      description: 'Security group for RDS PostgreSQL',
      allowAllOutbound: true,
    });

    const database = new rds.DatabaseInstance(this, 'ResilioDb', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_15,
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T3,
        ec2.InstanceSize.MICRO
      ),
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
      securityGroups: [dbSecurityGroup],
      databaseName: 'resilio',
      credentials: rds.Credentials.fromGeneratedSecret('resilio_admin', {
        secretName: 'resilio/database',
      }),
      allocatedStorage: 20,
      maxAllocatedStorage: 100,
      // Reliability improvements
      multiAz: true, // Automatic failover to standby in another AZ
      deleteAutomatedBackups: false, // Retain backups on deletion
      backupRetention: cdk.Duration.days(7), // 7-day backup retention
      removalPolicy: cdk.RemovalPolicy.RETAIN, // Don't delete database on stack deletion
      // Performance improvements
      enablePerformanceInsights: true, // Free tier: 7 days retention
      performanceInsightRetention: rds.PerformanceInsightRetention.DEFAULT, // 7 days (free tier)
    });

    // ========================================
    // Database Secret Rotation
    // ========================================
    // Enable automatic rotation of database credentials every 30 days
    // Uses AWS managed rotation Lambda for PostgreSQL
    database.addRotationSingleUser({
      automaticallyAfter: cdk.Duration.days(30),
      excludeCharacters: ' %+~`#$&*()|[]{}:;<>?!\'/@"\\',
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
    });

    // ========================================
    // ECS Cluster
    // ========================================
    const cluster = new ecs.Cluster(this, 'ResilioCluster', {
      vpc,
      containerInsightsV2: ecs.ContainerInsights.ENABLED,
    });

    // ========================================
    // Backend Docker Image
    // ========================================
    const backendImage = new ecr_assets.DockerImageAsset(this, 'BackendImage', {
      directory: '../backend',
      platform: ecr_assets.Platform.LINUX_AMD64,
    });

    // ========================================
    // Backend ECS Fargate Service
    // ========================================
    const backendService = new ecs_patterns.ApplicationLoadBalancedFargateService(
      this,
      'BackendService',
      {
        cluster,
        cpu: 256,
        memoryLimitMiB: 512,
        desiredCount: 2, // Minimum 2 tasks for high availability
        minHealthyPercent: 100, // Keep all tasks running during deployments
        maxHealthyPercent: 200, // Allow double capacity during deployments
        taskImageOptions: {
          image: ecs.ContainerImage.fromDockerImageAsset(backendImage),
          containerPort: 8000,
          environment: {
            DJANGO_SETTINGS_MODULE: 'config.settings',
            ALLOWED_HOSTS: '*',
            DEBUG: 'False',
            DB_NAME: 'resilio',
            DB_HOST: database.dbInstanceEndpointAddress,
            DB_PORT: database.dbInstanceEndpointPort,
            AWS_S3_BUCKET: 'dub01hackathongoal',
            AWS_S3_REGION: 'us-west-2',
          },
          secrets: {
            DB_USER: ecs.Secret.fromSecretsManager(database.secret!, 'username'),
            DB_PASSWORD: ecs.Secret.fromSecretsManager(database.secret!, 'password'),
            SECRET_KEY: ecs.Secret.fromSecretsManager(djangoSecret, 'secret_key'),
            AWS_ACCESS_KEY_ID: ecs.Secret.fromSecretsManager(s3UploadSecret, 'access_key_id'),
            AWS_SECRET_ACCESS_KEY: ecs.Secret.fromSecretsManager(s3UploadSecret, 'secret_access_key'),
            AWS_SESSION_TOKEN: ecs.Secret.fromSecretsManager(s3UploadSecret, 'session_token'),
          },
          logDriver: ecs.LogDrivers.awsLogs({
            streamPrefix: 'resilio-backend',
            logRetention: logs.RetentionDays.ONE_WEEK,
          }),
        },
        publicLoadBalancer: true,
        assignPublicIp: false,
      }
    );

    // Allow backend to connect to database
    dbSecurityGroup.addIngressRule(
      backendService.service.connections.securityGroups[0],
      ec2.Port.tcp(5432),
      'Allow backend to connect to database'
    );

    // Health check
    backendService.targetGroup.configureHealthCheck({
      path: '/api/health/',
      healthyHttpCodes: '200',
      interval: cdk.Duration.seconds(30),
      timeout: cdk.Duration.seconds(5),
    });

    // Grant backend task access to S3 upload bucket
    uploadBucket.grantReadWrite(backendService.taskDefinition.taskRole);

    // ========================================
    // ECS Auto Scaling
    // ========================================
    const scaling = backendService.service.autoScaleTaskCount({
      minCapacity: 2,
      maxCapacity: 10,
    });

    // Scale based on CPU utilization
    scaling.scaleOnCpuUtilization('CpuScaling', {
      targetUtilizationPercent: 70,
      scaleInCooldown: cdk.Duration.seconds(60),
      scaleOutCooldown: cdk.Duration.seconds(60),
    });

    // Scale based on memory utilization
    scaling.scaleOnMemoryUtilization('MemoryScaling', {
      targetUtilizationPercent: 70,
      scaleInCooldown: cdk.Duration.seconds(60),
      scaleOutCooldown: cdk.Duration.seconds(60),
    });

    // Scale based on request count per target
    scaling.scaleOnRequestCount('RequestScaling', {
      requestsPerTarget: 1000,
      targetGroup: backendService.targetGroup,
      scaleInCooldown: cdk.Duration.seconds(60),
      scaleOutCooldown: cdk.Duration.seconds(60),
    });

    // ========================================
    // Frontend S3 Bucket
    // ========================================
    const frontendBucket = new s3.Bucket(this, 'FrontendBucket', {
      bucketName: `resilio-frontend-${this.account}-${this.region}`,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.RETAIN, // Retain bucket on stack deletion
      versioned: true, // Enable versioning for data protection
    });

    // ========================================
    // Note: AWS WAF for CloudFront must be created in us-east-1 region
    // To add WAF protection, either:
    // 1. Create a separate CDK stack in us-east-1 with the WebACL
    // 2. Add WAF manually via AWS Console in us-east-1 and associate with CloudFront
    // Recommended managed rule sets:
    // - AWSManagedRulesCommonRuleSet (OWASP top 10 protection)
    // - AWSManagedRulesKnownBadInputsRuleSet (blocks known bad patterns)
    // - AWSManagedRulesSQLiRuleSet (SQL injection protection)
    // - Rate limiting rule (2000 req/5min per IP)
    // ========================================

    // ========================================
    // Security Response Headers Policy
    // ========================================
    const responseHeadersPolicy = new cloudfront.ResponseHeadersPolicy(this, 'SecurityHeadersPolicy', {
      responseHeadersPolicyName: 'ResilioSecurityHeaders',
      securityHeadersBehavior: {
        contentSecurityPolicy: {
          contentSecurityPolicy: "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https: http://*.elb.amazonaws.com;",
          override: true,
        },
        strictTransportSecurity: {
          accessControlMaxAge: cdk.Duration.days(365),
          includeSubdomains: true,
          preload: true,
          override: true,
        },
        contentTypeOptions: {
          override: true,
        },
        frameOptions: {
          frameOption: cloudfront.HeadersFrameOption.DENY,
          override: true,
        },
        xssProtection: {
          protection: true,
          modeBlock: true,
          override: true,
        },
        referrerPolicy: {
          referrerPolicy: cloudfront.HeadersReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN,
          override: true,
        },
      },
    });

    // ========================================
    // CloudFront Distribution
    // ========================================
    const distribution = new cloudfront.Distribution(this, 'FrontendDistribution', {
      defaultBehavior: {
        origin: cloudfront_origins.S3BucketOrigin.withOriginAccessControl(frontendBucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
        responseHeadersPolicy: responseHeadersPolicy,
      },
      additionalBehaviors: {
        '/api/*': {
          origin: new cloudfront_origins.HttpOrigin(
            backendService.loadBalancer.loadBalancerDnsName,
            {
              protocolPolicy: cloudfront.OriginProtocolPolicy.HTTP_ONLY,
            }
          ),
          viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
          originRequestPolicy: cloudfront.OriginRequestPolicy.ALL_VIEWER,
          allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
          responseHeadersPolicy: responseHeadersPolicy,
        },
      },
      defaultRootObject: 'index.html',
      errorResponses: [
        {
          httpStatus: 404,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
          ttl: cdk.Duration.minutes(5),
        },
      ],
    });

    // ========================================
    // CloudWatch Alarms for Performance Monitoring
    // ========================================

    // ALB Target Response Time alarm (latency > 1 second)
    new cloudwatch.Alarm(this, 'HighLatencyAlarm', {
      alarmName: 'Resilio-HighLatency',
      alarmDescription: 'API response time exceeds 1 second',
      metric: backendService.loadBalancer.metrics.targetResponseTime({
        period: cdk.Duration.minutes(1),
        statistic: 'Average',
      }),
      threshold: 1,
      evaluationPeriods: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });

    // ALB 5xx Error Rate alarm
    new cloudwatch.Alarm(this, 'High5xxErrorAlarm', {
      alarmName: 'Resilio-High5xxErrors',
      alarmDescription: 'High rate of 5xx errors from backend',
      metric: backendService.loadBalancer.metrics.httpCodeElb(
        cdk.aws_elasticloadbalancingv2.HttpCodeElb.ELB_5XX_COUNT,
        {
          period: cdk.Duration.minutes(5),
          statistic: 'Sum',
        }
      ),
      threshold: 10,
      evaluationPeriods: 2,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });

    // RDS CPU Utilization alarm
    new cloudwatch.Alarm(this, 'DatabaseHighCpuAlarm', {
      alarmName: 'Resilio-DatabaseHighCPU',
      alarmDescription: 'Database CPU utilization exceeds 80%',
      metric: database.metricCPUUtilization({
        period: cdk.Duration.minutes(5),
        statistic: 'Average',
      }),
      threshold: 80,
      evaluationPeriods: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });

    // RDS Free Storage Space alarm (< 5GB)
    new cloudwatch.Alarm(this, 'DatabaseLowStorageAlarm', {
      alarmName: 'Resilio-DatabaseLowStorage',
      alarmDescription: 'Database free storage space below 5GB',
      metric: database.metricFreeStorageSpace({
        period: cdk.Duration.minutes(5),
        statistic: 'Average',
      }),
      threshold: 5 * 1024 * 1024 * 1024, // 5GB in bytes
      evaluationPeriods: 2,
      comparisonOperator: cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });

    // RDS Database Connections alarm
    new cloudwatch.Alarm(this, 'DatabaseHighConnectionsAlarm', {
      alarmName: 'Resilio-DatabaseHighConnections',
      alarmDescription: 'Database connections exceeding 80% of max',
      metric: database.metricDatabaseConnections({
        period: cdk.Duration.minutes(5),
        statistic: 'Average',
      }),
      threshold: 80, // db.t3.micro max is ~87 connections
      evaluationPeriods: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });

    // ========================================
    // Outputs
    // ========================================
    new cdk.CfnOutput(this, 'VpcId', {
      value: vpc.vpcId,
      description: 'VPC ID',
    });

    new cdk.CfnOutput(this, 'DatabaseEndpoint', {
      value: database.dbInstanceEndpointAddress,
      description: 'RDS PostgreSQL endpoint',
    });

    new cdk.CfnOutput(this, 'BackendUrl', {
      value: `http://${backendService.loadBalancer.loadBalancerDnsName}`,
      description: 'Backend API URL',
    });

    new cdk.CfnOutput(this, 'FrontendBucketName', {
      value: frontendBucket.bucketName,
      description: 'Frontend S3 bucket name',
    });

    new cdk.CfnOutput(this, 'CloudFrontUrl', {
      value: `https://${distribution.distributionDomainName}`,
      description: 'CloudFront distribution URL',
    });

    new cdk.CfnOutput(this, 'CloudFrontDistributionId', {
      value: distribution.distributionId,
      description: 'CloudFront distribution ID',
    });

    new cdk.CfnOutput(this, 'S3UploadSecretArn', {
      value: s3UploadSecret.secretArn,
      description: 'ARN of the S3 upload credentials secret - update with your AWS credentials',
    });
  }
}
