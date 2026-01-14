<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'AWS Infrastructure - Documentation - Resilio',
})

const services = [
  {
    name: 'Amazon CloudFront',
    purpose: 'Global CDN for frontend assets and API proxy',
    details: 'Serves static assets with edge caching, routes /api/* requests to backend'
  },
  {
    name: 'Amazon S3',
    purpose: 'Static website hosting',
    details: 'Hosts the Nuxt-generated static files, not publicly accessible (CloudFront origin only)'
  },
  {
    name: 'Amazon ECS Fargate',
    purpose: 'Serverless container hosting',
    details: 'Runs Django application in containers, auto-scales based on load'
  },
  {
    name: 'Amazon RDS PostgreSQL',
    purpose: 'Managed database',
    details: 'Stores all application data with automated backups and Multi-AZ for production'
  },
  {
    name: 'Amazon Bedrock',
    purpose: 'AI/ML inference',
    details: 'Provides access to Claude Opus 4.5 for system analysis and chat'
  },
  {
    name: 'Application Load Balancer',
    purpose: 'Load balancing',
    details: 'Distributes traffic across ECS tasks, handles health checks'
  },
  {
    name: 'Amazon ECR',
    purpose: 'Container registry',
    details: 'Stores Docker images for the Django backend'
  },
  {
    name: 'AWS Secrets Manager',
    purpose: 'Secret storage',
    details: 'Securely stores database credentials, JWT secret, and API keys'
  },
  {
    name: 'Amazon VPC',
    purpose: 'Network isolation',
    details: 'Private subnets for ECS/RDS, public subnets for ALB'
  }
]
</script>

<template>
  <div>
    <Badge class="mb-4">Deployment</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">AWS Infrastructure</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Guide to deploying and managing Resilio on AWS using CDK.
    </p>

    <!-- Architecture Overview -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Architecture Overview</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-xs overflow-x-auto">
            <pre>
                                    ┌─────────────────┐
                                    │   CloudFront    │
                                    │   Distribution  │
                                    └────────┬────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
                    ▼                        ▼                        ▼
           ┌────────────────┐      ┌────────────────┐      ┌─────────────────┐
           │   S3 Bucket    │      │      ALB       │      │  CloudFront     │
           │   (Frontend)   │      │   (Backend)    │      │   Functions     │
           └────────────────┘      └───────┬────────┘      └─────────────────┘
                                           │
                                    ┌──────┴──────┐
                                    │             │
                              ┌─────┴─────┐ ┌─────┴─────┐
                              │  ECS Task │ │  ECS Task │
                              │  (Django) │ │  (Django) │
                              └─────┬─────┘ └─────┬─────┘
                                    │             │
                              ┌─────┴─────────────┴─────┐
                              │                         │
                        ┌─────┴─────┐           ┌───────┴───────┐
                        │    RDS    │           │    Bedrock    │
                        │ PostgreSQL│           │ (Claude Opus) │
                        └───────────┘           └───────────────┘</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- AWS Services -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">AWS Services Used</h2>
      <div class="space-y-4">
        <Card v-for="service in services" :key="service.name">
          <CardContent class="pt-6">
            <div class="flex flex-col md:flex-row md:items-start gap-4">
              <div class="flex-1">
                <h3 class="font-semibold text-goal-dark">{{ service.name }}</h3>
                <p class="text-sm text-muted-foreground mt-1">{{ service.purpose }}</p>
              </div>
              <div class="flex-1 text-sm text-muted-foreground">
                {{ service.details }}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Prerequisites -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Prerequisites</h2>
      <Card>
        <CardContent class="pt-6">
          <ul class="space-y-3">
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="mt-0.5">1</Badge>
              <div>
                <p class="font-medium">AWS Account with appropriate permissions</p>
                <p class="text-sm text-muted-foreground">IAM user/role with admin or specific CDK deployment permissions</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="mt-0.5">2</Badge>
              <div>
                <p class="font-medium">AWS CLI configured</p>
                <p class="text-sm text-muted-foreground">Run <code class="bg-muted px-1 rounded">aws configure</code> with your credentials</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="mt-0.5">3</Badge>
              <div>
                <p class="font-medium">Node.js 20+ and AWS CDK installed</p>
                <p class="text-sm text-muted-foreground">Run <code class="bg-muted px-1 rounded">npm install -g aws-cdk</code></p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="mt-0.5">4</Badge>
              <div>
                <p class="font-medium">Docker Desktop running</p>
                <p class="text-sm text-muted-foreground">Required for building container images</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="mt-0.5">5</Badge>
              <div>
                <p class="font-medium">Bedrock model access enabled</p>
                <p class="text-sm text-muted-foreground">Request access to Claude models in the AWS console (us-east-1 region)</p>
              </div>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>

    <!-- Deployment Steps -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Deployment Steps</h2>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <span class="flex h-6 w-6 items-center justify-center rounded-full bg-goal text-white text-sm">1</span>
            Bootstrap CDK (first time only)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>cd infra
npm install
npx cdk bootstrap aws://ACCOUNT_ID/us-west-2</pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <span class="flex h-6 w-6 items-center justify-center rounded-full bg-goal text-white text-sm">2</span>
            Deploy backend infrastructure
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>cd infra
npm run cdk deploy</pre>
          </div>
          <p class="text-sm text-muted-foreground mt-3">
            This deploys VPC, RDS, ECS, S3, and CloudFront in a single ResilioStack
          </p>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <span class="flex h-6 w-6 items-center justify-center rounded-full bg-goal text-white text-sm">3</span>
            Build and deploy frontend
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>cd frontend
npm run generate
aws s3 sync .output/public s3://resilio-frontend-ACCOUNT_ID-us-west-2 --delete</pre>
          </div>
          <p class="text-sm text-muted-foreground mt-3">
            Replace ACCOUNT_ID with your AWS account ID
          </p>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <span class="flex h-6 w-6 items-center justify-center rounded-full bg-goal text-white text-sm">4</span>
            Run database migrations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-slate-500"># Connect to ECS task and run migrations</span>
aws ecs execute-command \
  --cluster resilio-cluster \
  --task TASK_ID \
  --container django \
  --interactive \
  --command "/bin/bash"

<span class="text-slate-500"># Inside container:</span>
python manage.py migrate
python manage.py createsuperuser</pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <span class="flex h-6 w-6 items-center justify-center rounded-full bg-goal text-white text-sm">5</span>
            Invalidate CloudFront cache (after frontend updates)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>aws cloudfront create-invalidation \
  --distribution-id DISTRIBUTION_ID \
  --paths "/*"</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- CDK Stack Structure -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">CDK Stack Structure</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-cyan-400">infra/</span>
├── bin/
│   └── infra.ts               <span class="text-slate-500"># CDK app entry point</span>
├── lib/
│   └── infra-stack.ts         <span class="text-slate-500"># Single stack with all resources</span>
├── cdk.json
├── package.json
└── tsconfig.json

<span class="text-cyan-400">ResilioStack Resources:</span>
• VPC with public/private subnets
• RDS PostgreSQL with Secrets Manager auto-rotation
• ECS Fargate cluster with Django backend
• Application Load Balancer
• S3 bucket for static frontend hosting
• CloudFront distribution with API proxy
• Bedrock Runtime IAM permissions</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Environment Variables -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Environment Variables</h2>
      <Card>
        <CardHeader>
          <CardTitle>ECS Task Environment</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-slate-500"># Set via CDK or Secrets Manager</span>
DEBUG=False
SECRET_KEY=&lt;from-secrets-manager&gt;
ALLOWED_HOSTS=*.cloudfront.net

<span class="text-slate-500"># Database (from RDS)</span>
DB_HOST=&lt;rds-endpoint&gt;
DB_NAME=resilio
DB_USER=&lt;from-secrets-manager&gt;
DB_PASSWORD=&lt;from-secrets-manager&gt;
DB_PORT=5432

<span class="text-slate-500"># AWS</span>
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL=anthropic.claude-opus-4-5-20250514-v1:0</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Monitoring -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Monitoring & Logs</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <Card>
          <CardContent class="pt-6">
            <h3 class="font-semibold mb-2">CloudWatch Logs</h3>
            <p class="text-sm text-muted-foreground">
              ECS task logs are automatically sent to CloudWatch. View in the AWS console under
              <code class="bg-muted px-1 rounded">/ecs/resilio-backend</code>
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <h3 class="font-semibold mb-2">CloudFront Metrics</h3>
            <p class="text-sm text-muted-foreground">
              Monitor cache hit ratio, request counts, and error rates in CloudFront console
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <h3 class="font-semibold mb-2">RDS Performance</h3>
            <p class="text-sm text-muted-foreground">
              Database metrics available in RDS console including connections, CPU, and storage
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <h3 class="font-semibold mb-2">ECS Service Health</h3>
            <p class="text-sm text-muted-foreground">
              View task status, deployments, and health checks in ECS console
            </p>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Cost Estimation -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Cost Estimation</h2>
      <Card>
        <CardContent class="pt-6">
          <p class="text-muted-foreground mb-4">
            Estimated monthly costs for a small deployment (varies by usage):
          </p>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 text-sm font-medium text-muted-foreground">Service</th>
                  <th class="text-right py-2 text-sm font-medium text-muted-foreground">Est. Cost</th>
                </tr>
              </thead>
              <tbody class="text-sm">
                <tr class="border-b">
                  <td class="py-2">ECS Fargate (2 tasks, 0.5 vCPU, 1GB)</td>
                  <td class="py-2 text-right">~$30</td>
                </tr>
                <tr class="border-b">
                  <td class="py-2">RDS PostgreSQL (db.t3.micro)</td>
                  <td class="py-2 text-right">~$15</td>
                </tr>
                <tr class="border-b">
                  <td class="py-2">Application Load Balancer</td>
                  <td class="py-2 text-right">~$20</td>
                </tr>
                <tr class="border-b">
                  <td class="py-2">CloudFront (100GB transfer)</td>
                  <td class="py-2 text-right">~$10</td>
                </tr>
                <tr class="border-b">
                  <td class="py-2">S3 (minimal storage)</td>
                  <td class="py-2 text-right">~$1</td>
                </tr>
                <tr class="border-b">
                  <td class="py-2">Bedrock (varies by usage)</td>
                  <td class="py-2 text-right">~$20-100</td>
                </tr>
                <tr class="font-semibold">
                  <td class="py-2">Total (estimated)</td>
                  <td class="py-2 text-right">~$96-176/month</td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
