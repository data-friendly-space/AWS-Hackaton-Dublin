<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { CheckCircle, AlertTriangle, XCircle, Info } from 'lucide-vue-next'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'AWS Well-Architected Review - Documentation - Resilio',
})

type Status = 'good' | 'warning' | 'critical' | 'info'

interface Finding {
  title: string
  status: Status
  current: string
  recommendation: string
  priority: 'High' | 'Medium' | 'Low'
}

interface Pillar {
  name: string
  description: string
  score: number
  findings: Finding[]
}

const pillars: Pillar[] = [
  {
    name: 'Operational Excellence',
    description: 'Run and monitor systems to deliver business value and continually improve processes',
    score: 75,
    findings: [
      {
        title: 'Infrastructure as Code',
        status: 'good',
        current: 'All infrastructure defined in AWS CDK with TypeScript',
        recommendation: 'Continue using CDK for all infrastructure changes',
        priority: 'Low'
      },
      {
        title: 'Logging & Monitoring',
        status: 'good',
        current: 'CloudWatch Logs enabled for ECS tasks with 1-week retention, Container Insights enabled',
        recommendation: 'Consider extending log retention for production and adding CloudWatch alarms',
        priority: 'Medium'
      },
      {
        title: 'Health Checks',
        status: 'good',
        current: 'ALB health checks configured on /api/health/ endpoint',
        recommendation: 'Add deep health checks that verify database connectivity',
        priority: 'Low'
      },
      {
        title: 'Deployment Strategy',
        status: 'warning',
        current: 'Rolling deployments with minHealthyPercent not explicitly configured',
        recommendation: 'Configure minHealthyPercent to prevent downtime during deployments',
        priority: 'Medium'
      },
      {
        title: 'Runbooks & Documentation',
        status: 'warning',
        current: 'Basic deployment documentation exists',
        recommendation: 'Create operational runbooks for common failure scenarios',
        priority: 'Medium'
      }
    ]
  },
  {
    name: 'Security',
    description: 'Protect information, systems, and assets through risk assessments and mitigation strategies',
    score: 80,
    findings: [
      {
        title: 'Secrets Management',
        status: 'good',
        current: 'Database credentials, Django secret key, and S3 credentials stored in AWS Secrets Manager',
        recommendation: 'Enable automatic secret rotation for database credentials',
        priority: 'Medium'
      },
      {
        title: 'Network Isolation',
        status: 'good',
        current: 'VPC with public/private subnets, RDS in private subnet, ECS tasks in private subnet',
        recommendation: 'Current configuration is appropriate for the workload',
        priority: 'Low'
      },
      {
        title: 'HTTPS Enforcement',
        status: 'good',
        current: 'CloudFront enforces HTTPS redirect for all traffic',
        recommendation: 'Consider adding HSTS headers',
        priority: 'Low'
      },
      {
        title: 'Security Groups',
        status: 'good',
        current: 'Database only accessible from ECS tasks, ALB security group restricts inbound traffic',
        recommendation: 'Current configuration follows least privilege',
        priority: 'Low'
      },
      {
        title: 'S3 Bucket Security',
        status: 'good',
        current: 'Frontend bucket has BlockPublicAccess enabled, accessed only via CloudFront OAC',
        recommendation: 'Current configuration is secure',
        priority: 'Low'
      },
      {
        title: 'IAM Permissions',
        status: 'warning',
        current: 'ECS task role has S3 read/write access to upload bucket',
        recommendation: 'Review and scope down IAM permissions to specific prefixes if possible',
        priority: 'Low'
      },
      {
        title: 'ALB to Backend Communication',
        status: 'warning',
        current: 'CloudFront to ALB uses HTTP (not HTTPS)',
        recommendation: 'Consider enabling HTTPS between CloudFront and ALB for defense in depth',
        priority: 'Medium'
      },
      {
        title: 'WAF Protection',
        status: 'critical',
        current: 'No AWS WAF configured on CloudFront distribution',
        recommendation: 'Add AWS WAF with managed rule sets to protect against common attacks',
        priority: 'High'
      }
    ]
  },
  {
    name: 'Reliability',
    description: 'Recover from failures and meet demand through distributed system design',
    score: 55,
    findings: [
      {
        title: 'Multi-AZ Deployment',
        status: 'good',
        current: 'VPC spans 2 Availability Zones',
        recommendation: 'Current configuration provides basic redundancy',
        priority: 'Low'
      },
      {
        title: 'Database Backups',
        status: 'warning',
        current: 'RDS automated backups enabled but deleteAutomatedBackups=true set',
        recommendation: 'Disable deleteAutomatedBackups for production, enable point-in-time recovery',
        priority: 'High'
      },
      {
        title: 'Database High Availability',
        status: 'critical',
        current: 'Single-AZ RDS instance (no Multi-AZ)',
        recommendation: 'Enable Multi-AZ for production to provide automatic failover',
        priority: 'High'
      },
      {
        title: 'ECS Task Count',
        status: 'critical',
        current: 'Only 1 ECS task running (desiredCount: 1)',
        recommendation: 'Increase to minimum 2 tasks across AZs for high availability',
        priority: 'High'
      },
      {
        title: 'Auto Scaling',
        status: 'critical',
        current: 'No auto scaling configured for ECS service',
        recommendation: 'Add target tracking scaling policy based on CPU/memory utilization',
        priority: 'High'
      },
      {
        title: 'Data Retention',
        status: 'warning',
        current: 'S3 bucket has autoDeleteObjects=true and DESTROY removal policy',
        recommendation: 'Change to RETAIN for production and disable autoDeleteObjects',
        priority: 'High'
      },
      {
        title: 'NAT Gateway Redundancy',
        status: 'warning',
        current: 'Only 1 NAT Gateway configured',
        recommendation: 'Add NAT Gateway per AZ for high availability (cost consideration)',
        priority: 'Medium'
      }
    ]
  },
  {
    name: 'Performance Efficiency',
    description: 'Use computing resources efficiently to meet requirements and maintain efficiency',
    score: 70,
    findings: [
      {
        title: 'CDN Caching',
        status: 'good',
        current: 'CloudFront with CACHING_OPTIMIZED policy for static assets',
        recommendation: 'Current configuration is appropriate',
        priority: 'Low'
      },
      {
        title: 'API Caching',
        status: 'good',
        current: 'API routes have CACHING_DISABLED which is correct for dynamic content',
        recommendation: 'Consider caching specific read-only endpoints if performance requires',
        priority: 'Low'
      },
      {
        title: 'Database Instance Size',
        status: 'info',
        current: 'db.t3.micro instance type',
        recommendation: 'Monitor performance and scale up as needed; appropriate for development/hackathon',
        priority: 'Low'
      },
      {
        title: 'ECS Task Sizing',
        status: 'info',
        current: '256 CPU units, 512 MB memory',
        recommendation: 'Monitor resource utilization and adjust based on actual usage patterns',
        priority: 'Low'
      },
      {
        title: 'Database Storage',
        status: 'good',
        current: 'Storage auto-scaling enabled (20GB to 100GB)',
        recommendation: 'Current configuration handles growth automatically',
        priority: 'Low'
      },
      {
        title: 'Connection Pooling',
        status: 'warning',
        current: 'No RDS Proxy configured',
        recommendation: 'Add RDS Proxy if connection management becomes an issue at scale',
        priority: 'Low'
      }
    ]
  },
  {
    name: 'Cost Optimization',
    description: 'Avoid unnecessary costs and use the most cost-effective resources',
    score: 85,
    findings: [
      {
        title: 'Right-Sized Resources',
        status: 'good',
        current: 'Using smallest instance types (t3.micro for RDS, minimal Fargate)',
        recommendation: 'Appropriate for hackathon; monitor and scale as needed',
        priority: 'Low'
      },
      {
        title: 'Serverless Compute',
        status: 'good',
        current: 'Using Fargate (serverless) instead of EC2',
        recommendation: 'Pay only for what you use; good choice for variable workloads',
        priority: 'Low'
      },
      {
        title: 'NAT Gateway',
        status: 'info',
        current: 'Single NAT Gateway (~$32/month + data transfer)',
        recommendation: 'Consider NAT Instance for lower cost in dev environments',
        priority: 'Low'
      },
      {
        title: 'CloudFront Pricing',
        status: 'good',
        current: 'Using default price class (all edge locations)',
        recommendation: 'Consider PriceClass_100 to reduce costs if global coverage not needed',
        priority: 'Low'
      },
      {
        title: 'Log Retention',
        status: 'good',
        current: '1-week log retention minimizes storage costs',
        recommendation: 'Balance between cost and operational needs',
        priority: 'Low'
      },
      {
        title: 'Reserved Capacity',
        status: 'info',
        current: 'Using on-demand pricing for all resources',
        recommendation: 'Consider Savings Plans or Reserved Instances for production steady-state workloads',
        priority: 'Low'
      }
    ]
  },
  {
    name: 'Sustainability',
    description: 'Minimize environmental impact of cloud workloads',
    score: 75,
    findings: [
      {
        title: 'Serverless Architecture',
        status: 'good',
        current: 'Using Fargate and managed services reduces idle resources',
        recommendation: 'Serverless approach is inherently more sustainable',
        priority: 'Low'
      },
      {
        title: 'Region Selection',
        status: 'info',
        current: 'Deployed in us-west-2 (Oregon)',
        recommendation: 'Oregon has good renewable energy mix; consider user proximity',
        priority: 'Low'
      },
      {
        title: 'Static Asset Caching',
        status: 'good',
        current: 'CloudFront caching reduces origin requests',
        recommendation: 'Caching reduces compute and network energy consumption',
        priority: 'Low'
      },
      {
        title: 'Right-Sizing',
        status: 'good',
        current: 'Using minimal resources appropriate for workload',
        recommendation: 'Continue monitoring and right-sizing as usage patterns emerge',
        priority: 'Low'
      }
    ]
  }
]

const overallScore = Math.round(pillars.reduce((sum, p) => sum + p.score, 0) / pillars.length)

const criticalCount = pillars.reduce((sum, p) => sum + p.findings.filter(f => f.status === 'critical').length, 0)
const warningCount = pillars.reduce((sum, p) => sum + p.findings.filter(f => f.status === 'warning').length, 0)

function getStatusIcon(status: Status) {
  switch (status) {
    case 'good': return CheckCircle
    case 'warning': return AlertTriangle
    case 'critical': return XCircle
    case 'info': return Info
  }
}

function getStatusColor(status: Status) {
  switch (status) {
    case 'good': return 'text-green-600'
    case 'warning': return 'text-yellow-600'
    case 'critical': return 'text-red-600'
    case 'info': return 'text-blue-600'
  }
}

function getScoreColor(score: number) {
  if (score >= 80) return 'text-green-600'
  if (score >= 60) return 'text-yellow-600'
  return 'text-red-600'
}

function getPriorityVariant(priority: string): 'default' | 'secondary' | 'outline' | 'destructive' {
  switch (priority) {
    case 'High': return 'destructive'
    case 'Medium': return 'default'
    default: return 'secondary'
  }
}
</script>

<template>
  <div>
    <Badge class="mb-4">Audit</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">AWS Well-Architected Review</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Assessment of Resilio infrastructure against the AWS Well-Architected Framework pillars.
    </p>

    <!-- Executive Summary -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle>Executive Summary</CardTitle>
        <CardDescription>Overall assessment and key findings</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div :class="['text-5xl font-bold', getScoreColor(overallScore)]">{{ overallScore }}%</div>
            <p class="text-sm text-muted-foreground mt-1">Overall Score</p>
          </div>
          <div class="text-center">
            <div class="text-5xl font-bold text-red-600">{{ criticalCount }}</div>
            <p class="text-sm text-muted-foreground mt-1">Critical Issues</p>
          </div>
          <div class="text-center">
            <div class="text-5xl font-bold text-yellow-600">{{ warningCount }}</div>
            <p class="text-sm text-muted-foreground mt-1">Warnings</p>
          </div>
          <div class="text-center">
            <div class="text-5xl font-bold text-green-600">{{ pillars.length }}</div>
            <p class="text-sm text-muted-foreground mt-1">Pillars Reviewed</p>
          </div>
        </div>

        <div class="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <h4 class="font-semibold text-amber-800 mb-2">Key Recommendations</h4>
          <ul class="text-sm text-amber-700 space-y-1">
            <li>1. Enable Multi-AZ for RDS database for high availability</li>
            <li>2. Increase ECS task count to minimum 2 for redundancy</li>
            <li>3. Add auto-scaling policies for ECS service</li>
            <li>4. Configure AWS WAF on CloudFront for security</li>
            <li>5. Change removal policies from DESTROY to RETAIN for production</li>
          </ul>
        </div>
      </CardContent>
    </Card>

    <!-- Pillar Scores Overview -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Pillar Scores</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <Card v-for="pillar in pillars" :key="pillar.name">
          <CardContent class="pt-6 text-center">
            <div :class="['text-3xl font-bold', getScoreColor(pillar.score)]">{{ pillar.score }}%</div>
            <p class="text-xs text-muted-foreground mt-1">{{ pillar.name.split(' ')[0] }}</p>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Detailed Findings by Pillar -->
    <div class="space-y-8">
      <div v-for="pillar in pillars" :key="pillar.name">
        <Card>
          <CardHeader>
            <div class="flex items-center justify-between">
              <div>
                <CardTitle>{{ pillar.name }}</CardTitle>
                <CardDescription>{{ pillar.description }}</CardDescription>
              </div>
              <div :class="['text-3xl font-bold', getScoreColor(pillar.score)]">
                {{ pillar.score }}%
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <div
                v-for="finding in pillar.findings"
                :key="finding.title"
                class="border rounded-lg p-4"
              >
                <div class="flex items-start gap-3">
                  <component
                    :is="getStatusIcon(finding.status)"
                    :class="['h-5 w-5 mt-0.5 flex-shrink-0', getStatusColor(finding.status)]"
                  />
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-1">
                      <h4 class="font-semibold">{{ finding.title }}</h4>
                      <Badge :variant="getPriorityVariant(finding.priority)" class="text-xs">
                        {{ finding.priority }}
                      </Badge>
                    </div>
                    <div class="text-sm space-y-2">
                      <p><span class="text-muted-foreground">Current:</span> {{ finding.current }}</p>
                      <p><span class="text-muted-foreground">Recommendation:</span> {{ finding.recommendation }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Production Readiness Checklist -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Production Readiness Checklist</CardTitle>
        <CardDescription>Critical items to address before production deployment</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-3">
          <div class="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
            <XCircle class="h-5 w-5 text-red-600" />
            <span class="text-sm">Enable RDS Multi-AZ deployment</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
            <XCircle class="h-5 w-5 text-red-600" />
            <span class="text-sm">Increase ECS desired count to 2+</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
            <XCircle class="h-5 w-5 text-red-600" />
            <span class="text-sm">Configure ECS auto-scaling policies</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
            <XCircle class="h-5 w-5 text-red-600" />
            <span class="text-sm">Add AWS WAF to CloudFront distribution</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
            <AlertTriangle class="h-5 w-5 text-yellow-600" />
            <span class="text-sm">Change S3 removal policy from DESTROY to RETAIN</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
            <AlertTriangle class="h-5 w-5 text-yellow-600" />
            <span class="text-sm">Disable deleteAutomatedBackups for RDS</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
            <AlertTriangle class="h-5 w-5 text-yellow-600" />
            <span class="text-sm">Configure HTTPS between CloudFront and ALB</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
            <AlertTriangle class="h-5 w-5 text-yellow-600" />
            <span class="text-sm">Set minHealthyPercent for rolling deployments</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">Secrets stored in AWS Secrets Manager</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">Database in private subnet</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">HTTPS enforced via CloudFront</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">Infrastructure as Code (CDK)</span>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Review Metadata -->
    <div class="mt-8 text-sm text-muted-foreground">
      <p>Review Date: January 2026</p>
      <p>AWS Region: us-west-2</p>
      <p>Framework Version: AWS Well-Architected Framework (2024)</p>
    </div>
  </div>
</template>
