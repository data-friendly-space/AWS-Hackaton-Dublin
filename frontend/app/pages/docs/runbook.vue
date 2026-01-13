<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlertTriangle, CheckCircle, Database, Server, Globe, Shield, Activity, Clock } from 'lucide-vue-next'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'Operations Runbook - Documentation - Resilio',
})
</script>

<template>
  <div>
    <Badge class="mb-4">Operations</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">Operations Runbook</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Comprehensive guide for operating and troubleshooting the Resilio platform.
    </p>

    <!-- Quick Reference -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle>Quick Reference</CardTitle>
        <CardDescription>Essential information for on-call operators</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 bg-muted rounded-lg">
            <h4 class="font-semibold mb-2">Key Resources</h4>
            <ul class="text-sm space-y-1">
              <li><strong>CloudFront URL:</strong> https://d18cm0umrsa2ex.cloudfront.net</li>
              <li><strong>AWS Region:</strong> us-west-2</li>
              <li><strong>Stack Name:</strong> ResilioStack</li>
              <li><strong>CloudWatch Dashboard:</strong> ResilioStack alarms</li>
            </ul>
          </div>
          <div class="p-4 bg-muted rounded-lg">
            <h4 class="font-semibold mb-2">Escalation Contacts</h4>
            <ul class="text-sm space-y-1">
              <li><strong>Primary:</strong> Platform Team</li>
              <li><strong>AWS Support:</strong> AWS Console → Support Center</li>
              <li><strong>GitHub Issues:</strong> data-friendly-space/AWS-Hackaton-Dublin</li>
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- CloudWatch Alarms -->
    <Card class="mb-8">
      <CardHeader>
        <div class="flex items-center gap-2">
          <Activity class="h-5 w-5 text-goal-orange" />
          <CardTitle>CloudWatch Alarms</CardTitle>
        </div>
        <CardDescription>Configured alarms and response procedures</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-6">
          <!-- High Latency Alarm -->
          <div class="border rounded-lg p-4">
            <div class="flex items-center gap-2 mb-3">
              <AlertTriangle class="h-5 w-5 text-yellow-600" />
              <h4 class="font-semibold">Resilio-HighLatency</h4>
              <Badge variant="outline">Warning</Badge>
            </div>
            <p class="text-sm text-muted-foreground mb-3">
              <strong>Trigger:</strong> Average API response time exceeds 1 second for 3 consecutive minutes
            </p>
            <div class="bg-muted p-3 rounded text-sm">
              <p class="font-semibold mb-2">Response Procedure:</p>
              <ol class="list-decimal list-inside space-y-1">
                <li>Check ECS task count - may need to scale up</li>
                <li>Check RDS Performance Insights for slow queries</li>
                <li>Review CloudWatch Logs for error patterns</li>
                <li>Check database CPU and connection count</li>
                <li>If persistent, consider scaling ECS tasks or RDS instance</li>
              </ol>
            </div>
          </div>

          <!-- 5xx Errors Alarm -->
          <div class="border rounded-lg p-4">
            <div class="flex items-center gap-2 mb-3">
              <AlertTriangle class="h-5 w-5 text-red-600" />
              <h4 class="font-semibold">Resilio-High5xxErrors</h4>
              <Badge variant="destructive">Critical</Badge>
            </div>
            <p class="text-sm text-muted-foreground mb-3">
              <strong>Trigger:</strong> More than 10 5xx errors in 5 minutes
            </p>
            <div class="bg-muted p-3 rounded text-sm">
              <p class="font-semibold mb-2">Response Procedure:</p>
              <ol class="list-decimal list-inside space-y-1">
                <li>Check ECS task health in AWS Console</li>
                <li>Review CloudWatch Logs for stack traces</li>
                <li>Check if recent deployment occurred</li>
                <li>Verify database connectivity</li>
                <li>If deployment issue, rollback using CDK</li>
                <li>If persistent, restart ECS tasks</li>
              </ol>
            </div>
          </div>

          <!-- Database CPU Alarm -->
          <div class="border rounded-lg p-4">
            <div class="flex items-center gap-2 mb-3">
              <Database class="h-5 w-5 text-yellow-600" />
              <h4 class="font-semibold">Resilio-DatabaseHighCPU</h4>
              <Badge variant="outline">Warning</Badge>
            </div>
            <p class="text-sm text-muted-foreground mb-3">
              <strong>Trigger:</strong> Database CPU exceeds 80% for 15 minutes
            </p>
            <div class="bg-muted p-3 rounded text-sm">
              <p class="font-semibold mb-2">Response Procedure:</p>
              <ol class="list-decimal list-inside space-y-1">
                <li>Open RDS Performance Insights</li>
                <li>Identify top queries by load</li>
                <li>Check for missing indexes or full table scans</li>
                <li>Review recent application changes</li>
                <li>Consider adding indexes or optimizing queries</li>
                <li>If growth-related, plan instance upgrade</li>
              </ol>
            </div>
          </div>

          <!-- Database Storage Alarm -->
          <div class="border rounded-lg p-4">
            <div class="flex items-center gap-2 mb-3">
              <Database class="h-5 w-5 text-red-600" />
              <h4 class="font-semibold">Resilio-DatabaseLowStorage</h4>
              <Badge variant="destructive">Critical</Badge>
            </div>
            <p class="text-sm text-muted-foreground mb-3">
              <strong>Trigger:</strong> Free storage space below 5GB
            </p>
            <div class="bg-muted p-3 rounded text-sm">
              <p class="font-semibold mb-2">Response Procedure:</p>
              <ol class="list-decimal list-inside space-y-1">
                <li>Storage auto-scaling should handle this automatically (up to 100GB)</li>
                <li>If at 100GB limit, manually increase maxAllocatedStorage in CDK</li>
                <li>Identify large tables: SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_stat_user_tables ORDER BY pg_total_relation_size(relid) DESC;</li>
                <li>Consider archiving old data if applicable</li>
                <li>Review and clean up unused indexes</li>
              </ol>
            </div>
          </div>

          <!-- Database Connections Alarm -->
          <div class="border rounded-lg p-4">
            <div class="flex items-center gap-2 mb-3">
              <Database class="h-5 w-5 text-yellow-600" />
              <h4 class="font-semibold">Resilio-DatabaseHighConnections</h4>
              <Badge variant="outline">Warning</Badge>
            </div>
            <p class="text-sm text-muted-foreground mb-3">
              <strong>Trigger:</strong> Database connections exceed 80 (db.t3.micro limit ~87)
            </p>
            <div class="bg-muted p-3 rounded text-sm">
              <p class="font-semibold mb-2">Response Procedure:</p>
              <ol class="list-decimal list-inside space-y-1">
                <li>Check ECS task count - may have scaled too high</li>
                <li>Review application connection pooling settings</li>
                <li>Identify connections: SELECT * FROM pg_stat_activity;</li>
                <li>Kill idle connections if necessary</li>
                <li>Consider adding RDS Proxy for connection pooling</li>
                <li>If growth-related, upgrade to larger instance</li>
              </ol>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Common Operations -->
    <Card class="mb-8">
      <CardHeader>
        <div class="flex items-center gap-2">
          <Server class="h-5 w-5 text-goal-orange" />
          <CardTitle>Common Operations</CardTitle>
        </div>
        <CardDescription>Step-by-step procedures for routine tasks</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-6">
          <!-- Deploy Application -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3">Deploy Application Changes</h4>
            <div class="bg-gray-900 text-gray-100 p-4 rounded-lg text-sm font-mono overflow-x-auto">
              <pre># 1. Deploy backend (from infra directory)
cd infra
AWS_PROFILE=resilio npm run cdk deploy

# 2. Build and deploy frontend
cd ../frontend
npm run generate
aws --profile resilio s3 sync .output/public s3://resilio-frontend-460832197675-us-west-2 --delete

# 3. Invalidate CloudFront cache
aws --profile resilio cloudfront create-invalidation \
  --distribution-id E1YGYTO8BUKMTV \
  --paths "/*"</pre>
            </div>
          </div>

          <!-- View Logs -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3">View Application Logs</h4>
            <div class="bg-gray-900 text-gray-100 p-4 rounded-lg text-sm font-mono overflow-x-auto">
              <pre># View recent logs
aws --profile resilio logs tail /ecs/resilio-backend --follow

# Search for errors
aws --profile resilio logs filter-log-events \
  --log-group-name /ecs/resilio-backend \
  --filter-pattern "ERROR" \
  --start-time $(date -v-1H +%s000)

# View in CloudWatch Console
# Navigate to: CloudWatch → Log groups → /ecs/resilio-backend</pre>
            </div>
          </div>

          <!-- Restart ECS Tasks -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3">Restart ECS Tasks</h4>
            <div class="bg-gray-900 text-gray-100 p-4 rounded-lg text-sm font-mono overflow-x-auto">
              <pre># Force new deployment (rolling restart)
aws --profile resilio ecs update-service \
  --cluster ResilioCluster \
  --service BackendService \
  --force-new-deployment

# Monitor deployment
aws --profile resilio ecs describe-services \
  --cluster ResilioCluster \
  --services BackendService \
  --query 'services[0].deployments'</pre>
            </div>
          </div>

          <!-- Scale ECS -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3">Manually Scale ECS Tasks</h4>
            <div class="bg-gray-900 text-gray-100 p-4 rounded-lg text-sm font-mono overflow-x-auto">
              <pre># Scale to specific count (2-10 range)
aws --profile resilio ecs update-service \
  --cluster ResilioCluster \
  --service BackendService \
  --desired-count 4

# Note: Auto-scaling will adjust based on metrics
# To permanently change, update CDK and redeploy</pre>
            </div>
          </div>

          <!-- Database Operations -->
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3">Database Operations</h4>
            <div class="bg-gray-900 text-gray-100 p-4 rounded-lg text-sm font-mono overflow-x-auto">
              <pre># Get database credentials
aws --profile resilio secretsmanager get-secret-value \
  --secret-id resilio/database \
  --query SecretString --output text | jq

# Connect via bastion (if configured) or use Query Editor
# AWS Console → RDS → Query Editor

# Manual secret rotation (if needed)
aws --profile resilio secretsmanager rotate-secret \
  --secret-id resilio/database

# View Performance Insights
# AWS Console → RDS → Performance Insights</pre>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Incident Response -->
    <Card class="mb-8">
      <CardHeader>
        <div class="flex items-center gap-2">
          <Shield class="h-5 w-5 text-goal-orange" />
          <CardTitle>Incident Response</CardTitle>
        </div>
        <CardDescription>Procedures for handling incidents</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-6">
          <!-- Service Outage -->
          <div class="border border-red-200 rounded-lg p-4 bg-red-50">
            <h4 class="font-semibold text-red-800 mb-3">Complete Service Outage</h4>
            <ol class="list-decimal list-inside space-y-2 text-sm">
              <li><strong>Verify outage:</strong> Check CloudFront URL and ALB health</li>
              <li><strong>Check ECS:</strong> Verify tasks are running in AWS Console</li>
              <li><strong>Check RDS:</strong> Verify database is available</li>
              <li><strong>Review CloudWatch:</strong> Check for alarm triggers</li>
              <li><strong>Check recent changes:</strong> Review recent deployments</li>
              <li><strong>Rollback if needed:</strong> Use git revert and redeploy</li>
              <li><strong>Communicate:</strong> Update stakeholders on status</li>
            </ol>
          </div>

          <!-- Database Failure -->
          <div class="border border-yellow-200 rounded-lg p-4 bg-yellow-50">
            <h4 class="font-semibold text-yellow-800 mb-3">Database Connectivity Issues</h4>
            <ol class="list-decimal list-inside space-y-2 text-sm">
              <li><strong>Check RDS status:</strong> AWS Console → RDS → Databases</li>
              <li><strong>Verify Multi-AZ:</strong> Check if failover occurred</li>
              <li><strong>Check security groups:</strong> Verify ECS can reach RDS</li>
              <li><strong>Review credentials:</strong> Check if rotation recently occurred</li>
              <li><strong>Restart ECS tasks:</strong> Force new deployment to refresh connections</li>
              <li><strong>If corruption:</strong> Restore from automated backup</li>
            </ol>
          </div>

          <!-- High Traffic -->
          <div class="border border-blue-200 rounded-lg p-4 bg-blue-50">
            <h4 class="font-semibold text-blue-800 mb-3">High Traffic / Load</h4>
            <ol class="list-decimal list-inside space-y-2 text-sm">
              <li><strong>Monitor auto-scaling:</strong> ECS should scale automatically</li>
              <li><strong>Check CloudFront:</strong> Verify caching is working</li>
              <li><strong>Manual scale:</strong> Increase desired count if needed</li>
              <li><strong>Database load:</strong> Monitor connections and CPU</li>
              <li><strong>If sustained:</strong> Consider instance upgrades</li>
            </ol>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Disaster Recovery -->
    <Card class="mb-8">
      <CardHeader>
        <div class="flex items-center gap-2">
          <Clock class="h-5 w-5 text-goal-orange" />
          <CardTitle>Disaster Recovery</CardTitle>
        </div>
        <CardDescription>Recovery procedures for major failures</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-6">
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3">Database Recovery</h4>
            <div class="text-sm space-y-3">
              <p><strong>RTO:</strong> ~15 minutes (Multi-AZ automatic failover)</p>
              <p><strong>RPO:</strong> 0 (synchronous replication to standby)</p>
              <div class="bg-muted p-3 rounded">
                <p class="font-semibold mb-2">Point-in-Time Recovery:</p>
                <ol class="list-decimal list-inside space-y-1">
                  <li>Go to RDS → Databases → Select instance</li>
                  <li>Actions → Restore to point in time</li>
                  <li>Select target time (within 7-day retention)</li>
                  <li>Create new instance with recovered data</li>
                  <li>Update CDK to point to new instance</li>
                  <li>Redeploy application</li>
                </ol>
              </div>
            </div>
          </div>

          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-3">Full Stack Recovery</h4>
            <div class="text-sm space-y-3">
              <p>If the entire stack needs to be recreated:</p>
              <div class="bg-gray-900 text-gray-100 p-4 rounded-lg font-mono overflow-x-auto">
                <pre># 1. Ensure code is up to date
git pull origin main

# 2. Deploy infrastructure
cd infra
AWS_PROFILE=resilio npm run cdk deploy

# 3. Restore database from backup (if needed)
# Use AWS Console or CLI to restore RDS

# 4. Deploy frontend
cd ../frontend
npm run generate
aws --profile resilio s3 sync .output/public s3://BUCKET_NAME --delete

# 5. Update DNS/CloudFront if distribution changed</pre>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Maintenance Windows -->
    <Card class="mb-8">
      <CardHeader>
        <div class="flex items-center gap-2">
          <Globe class="h-5 w-5 text-goal-orange" />
          <CardTitle>Scheduled Maintenance</CardTitle>
        </div>
        <CardDescription>Routine maintenance procedures</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-2">Secret Rotation</h4>
            <p class="text-sm text-muted-foreground mb-2">
              Database credentials are automatically rotated every 30 days. The rotation Lambda handles this seamlessly.
            </p>
            <p class="text-sm"><strong>Impact:</strong> None (ECS tasks automatically get new credentials)</p>
          </div>

          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-2">RDS Maintenance Window</h4>
            <p class="text-sm text-muted-foreground mb-2">
              AWS applies patches during the maintenance window. Multi-AZ ensures minimal downtime.
            </p>
            <p class="text-sm"><strong>Impact:</strong> Brief failover (~60 seconds) during patching</p>
          </div>

          <div class="border rounded-lg p-4">
            <h4 class="font-semibold mb-2">Log Retention</h4>
            <p class="text-sm text-muted-foreground mb-2">
              CloudWatch logs are retained for 7 days. Older logs are automatically deleted.
            </p>
            <p class="text-sm"><strong>Action:</strong> Export important logs before expiration if needed</p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Contacts and Resources -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle>Additional Resources</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 border rounded-lg">
            <h4 class="font-semibold mb-2">AWS Documentation</h4>
            <ul class="text-sm space-y-1">
              <li><a href="https://docs.aws.amazon.com/ecs/" class="text-blue-600 hover:underline">ECS Documentation</a></li>
              <li><a href="https://docs.aws.amazon.com/rds/" class="text-blue-600 hover:underline">RDS Documentation</a></li>
              <li><a href="https://docs.aws.amazon.com/cloudfront/" class="text-blue-600 hover:underline">CloudFront Documentation</a></li>
            </ul>
          </div>
          <div class="p-4 border rounded-lg">
            <h4 class="font-semibold mb-2">Project Resources</h4>
            <ul class="text-sm space-y-1">
              <li><a href="/docs/architecture" class="text-blue-600 hover:underline">Architecture Overview</a></li>
              <li><a href="/docs/aws" class="text-blue-600 hover:underline">AWS Deployment Guide</a></li>
              <li><a href="/docs/well-architected" class="text-blue-600 hover:underline">Well-Architected Review</a></li>
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Review Metadata -->
    <div class="mt-8 text-sm text-muted-foreground">
      <p>Last Updated: January 2026</p>
      <p>AWS Region: us-west-2</p>
    </div>
  </div>
</template>
