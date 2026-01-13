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
    score: 85,
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
        status: 'good',
        current: 'Rolling deployments with minHealthyPercent=100%, maxHealthyPercent=200% configured',
        recommendation: 'Current configuration ensures zero-downtime deployments',
        priority: 'Low'
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
    score: 90,
    findings: [
      {
        title: 'Security Headers',
        status: 'good',
        current: 'CloudFront response headers policy with HSTS, CSP, X-Frame-Options, X-Content-Type-Options, XSS-Protection, Referrer-Policy',
        recommendation: 'Current configuration provides defense-in-depth against common web vulnerabilities',
        priority: 'Low'
      },
      {
        title: 'WAF Protection',
        status: 'warning',
        current: 'AWS WAF not yet configured (requires separate us-east-1 deployment for CloudFront)',
        recommendation: 'Add AWS WAF via Console or separate CDK stack in us-east-1 with managed rule sets',
        priority: 'Medium'
      },
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
        current: 'CloudFront enforces HTTPS redirect with HSTS preload for all traffic',
        recommendation: 'Current configuration enforces secure connections',
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
        status: 'good',
        current: 'ECS task role has S3 read/write access scoped to specific upload bucket only',
        recommendation: 'Current configuration follows least privilege for the use case',
        priority: 'Low'
      },
      {
        title: 'CloudFront to ALB Communication',
        status: 'info',
        current: 'CloudFront to ALB uses HTTP within AWS network',
        recommendation: 'Enable HTTPS on ALB when custom domain is configured (requires ACM certificate)',
        priority: 'Low'
      }
    ]
  },
  {
    name: 'Reliability',
    description: 'Recover from failures and meet demand through distributed system design',
    score: 95,
    findings: [
      {
        title: 'Multi-AZ Deployment',
        status: 'good',
        current: 'VPC spans 2 Availability Zones with NAT Gateway in each AZ',
        recommendation: 'Current configuration provides full AZ redundancy',
        priority: 'Low'
      },
      {
        title: 'Database Backups',
        status: 'good',
        current: 'RDS automated backups enabled with 7-day retention, deleteAutomatedBackups=false',
        recommendation: 'Current configuration provides point-in-time recovery capability',
        priority: 'Low'
      },
      {
        title: 'Database High Availability',
        status: 'good',
        current: 'Multi-AZ RDS deployment with automatic failover to standby',
        recommendation: 'Current configuration provides automatic failover capability',
        priority: 'Low'
      },
      {
        title: 'ECS Task Count',
        status: 'good',
        current: 'Minimum 2 ECS tasks running across AZs (desiredCount: 2)',
        recommendation: 'Current configuration provides redundancy across availability zones',
        priority: 'Low'
      },
      {
        title: 'Auto Scaling',
        status: 'good',
        current: 'Auto scaling configured: CPU (70%), Memory (70%), Request count (1000/target), scales 2-10 tasks',
        recommendation: 'Current configuration handles load spikes automatically',
        priority: 'Low'
      },
      {
        title: 'Data Retention',
        status: 'good',
        current: 'S3 bucket with RETAIN removal policy and versioning enabled',
        recommendation: 'Current configuration protects against accidental deletion',
        priority: 'Low'
      },
      {
        title: 'NAT Gateway Redundancy',
        status: 'good',
        current: '2 NAT Gateways configured (one per AZ)',
        recommendation: 'Current configuration provides full network redundancy',
        priority: 'Low'
      }
    ]
  },
  {
    name: 'Performance Efficiency',
    description: 'Use computing resources efficiently to meet requirements and maintain efficiency',
    score: 85,
    findings: [
      {
        title: 'Performance Monitoring',
        status: 'good',
        current: 'CloudWatch alarms for latency (>1s), 5xx errors (>10/5min), DB CPU (>80%), storage (<5GB), connections (>80)',
        recommendation: 'Comprehensive monitoring enables proactive performance management',
        priority: 'Low'
      },
      {
        title: 'Database Performance Insights',
        status: 'good',
        current: 'RDS Performance Insights enabled with 7-day retention (free tier)',
        recommendation: 'Use Performance Insights to identify slow queries and bottlenecks',
        priority: 'Low'
      },
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
        current: '256 CPU units, 512 MB memory with Container Insights enabled',
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
        status: 'info',
        current: 'No RDS Proxy configured; connection alarm at 80 connections',
        recommendation: 'Add RDS Proxy if connection limit is reached at scale',
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
        current: '2 NAT Gateways for HA (~$64/month + data transfer)',
        recommendation: 'Cost of HA; consider single NAT Gateway for dev environments',
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

        <div class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <h4 class="font-semibold text-green-800 mb-2">Recent Improvements</h4>
          <ul class="text-sm text-green-700 space-y-1">
            <li>✓ CloudWatch alarms for latency, errors, DB CPU, storage, and connections</li>
            <li>✓ RDS Performance Insights enabled (7-day retention)</li>
            <li>✓ Security headers policy (HSTS, CSP, X-Frame-Options, XSS-Protection, Referrer-Policy)</li>
            <li>✓ RDS Multi-AZ deployment enabled for automatic failover</li>
            <li>✓ ECS task count increased to 2 with auto-scaling (2-10 tasks)</li>
            <li>✓ NAT Gateway redundancy (one per AZ)</li>
            <li>✓ S3 versioning and RETAIN policy for data protection</li>
            <li>✓ Database backup retention set to 7 days</li>
          </ul>
        </div>

        <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 class="font-semibold text-blue-800 mb-2">Future Considerations</h4>
          <ul class="text-sm text-blue-700 space-y-1">
            <li>• Add AWS WAF (requires us-east-1 deployment for CloudFront)</li>
            <li>• Enable HTTPS on ALB when custom domain is configured</li>
            <li>• Enable automatic secret rotation for database credentials</li>
            <li>• Create operational runbooks for failure scenarios</li>
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
        <CardDescription>Status of critical production requirements</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-3">
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">RDS Multi-AZ deployment enabled</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">ECS desired count set to 2+ with auto-scaling</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">ECS auto-scaling policies configured (CPU, Memory, Requests)</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">S3 removal policy set to RETAIN with versioning</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">RDS backups retained with 7-day retention</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">minHealthyPercent configured for zero-downtime deployments</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">NAT Gateway redundancy (one per AZ)</span>
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
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">Security headers (HSTS, CSP, X-Frame-Options, XSS-Protection)</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">CloudWatch alarms for performance monitoring</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <CheckCircle class="h-5 w-5 text-green-600" />
            <span class="text-sm">RDS Performance Insights enabled</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
            <AlertTriangle class="h-5 w-5 text-yellow-600" />
            <span class="text-sm">AWS WAF (requires us-east-1 deployment)</span>
          </div>
          <div class="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
            <Info class="h-5 w-5 text-blue-600" />
            <span class="text-sm">CloudFront-ALB HTTPS (requires custom domain)</span>
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
