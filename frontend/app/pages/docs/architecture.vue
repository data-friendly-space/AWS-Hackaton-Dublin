<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'Architecture - Documentation - Resilio',
})

const awsServices = [
  { service: 'CloudFront', purpose: 'CDN for static frontend + API proxy', category: 'Networking' },
  { service: 'S3', purpose: 'Static website hosting', category: 'Storage' },
  { service: 'ECS Fargate', purpose: 'Containerized Django backend', category: 'Compute' },
  { service: 'RDS PostgreSQL', purpose: 'Relational database', category: 'Database' },
  { service: 'Application Load Balancer', purpose: 'Backend traffic routing', category: 'Networking' },
  { service: 'VPC', purpose: 'Network isolation (public/private subnets)', category: 'Networking' },
  { service: 'Secrets Manager', purpose: 'Database credentials storage', category: 'Security' },
  { service: 'Amazon Bedrock', purpose: 'AI/ML inference (Claude Opus 4.5)', category: 'AI/ML' },
]

const categoryColors: Record<string, string> = {
  Networking: 'bg-blue-100 text-blue-700',
  Storage: 'bg-amber-100 text-amber-700',
  Compute: 'bg-green-100 text-green-700',
  Database: 'bg-purple-100 text-purple-700',
  Security: 'bg-red-100 text-red-700',
  'AI/ML': 'bg-cyan-100 text-cyan-700',
}
</script>

<template>
  <div>
    <Badge class="mb-4">Getting Started</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">Architecture</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Resilio is built on a modern, serverless-first AWS architecture designed for scalability and cost efficiency.
    </p>

    <!-- Architecture Diagram -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle>System Architecture</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="bg-slate-900 text-green-400 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>
┌─────────────────────────────────────────────────────────────────┐
│                        CloudFront CDN                           │
│                   (d18cm0umrsa2ex.cloudfront.net)               │
├─────────────────────────────────────────────────────────────────┤
│                              │                                   │
│    ┌─────────────────────┐   │   ┌─────────────────────────┐    │
│    │   S3 Static Site    │   │   │   Application Load      │    │
│    │   (Nuxt 3 SSG)      │◄──┼───┤   Balancer (/api/*)     │    │
│    └─────────────────────┘   │   └───────────┬─────────────┘    │
│                              │               │                   │
│                              │   ┌───────────▼─────────────┐    │
│                              │   │   ECS Fargate           │    │
│                              │   │   (Django REST API)     │    │
│                              │   └───────────┬─────────────┘    │
│                              │               │                   │
│                              │   ┌───────────▼─────────────┐    │
│                              │   │   RDS PostgreSQL        │    │
│                              │   │   (Private Subnet)      │    │
│                              │   └─────────────────────────┘    │
│                              │                                   │
│                              │   ┌─────────────────────────┐    │
│                              │   │   Amazon Bedrock        │    │
│                              │   │   (Claude Opus 4.5)     │    │
│                              │   └─────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘</pre>
        </div>
      </CardContent>
    </Card>

    <!-- Data Flow -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Data Flow</h2>
      <div class="prose prose-slate max-w-none">
        <ol class="space-y-3">
          <li>
            <strong>User Request</strong> - All requests hit CloudFront CDN first for caching and SSL termination
          </li>
          <li>
            <strong>Static Content</strong> - Frontend assets (HTML, JS, CSS) served directly from S3
          </li>
          <li>
            <strong>API Requests</strong> - Requests to <code>/api/*</code> are proxied through ALB to ECS Fargate
          </li>
          <li>
            <strong>Authentication</strong> - JWT tokens validated by Django REST Framework
          </li>
          <li>
            <strong>Database</strong> - PostgreSQL in private subnet, accessed only by ECS tasks
          </li>
          <li>
            <strong>AI Analysis</strong> - Claude Opus 4.5 invoked via Amazon Bedrock for system analysis
          </li>
        </ol>
      </div>
    </div>

    <!-- AWS Services -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">AWS Services Used</h2>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b">
              <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Service</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Category</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Purpose</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in awsServices" :key="item.service" class="border-b last:border-0 hover:bg-muted/50">
              <td class="py-3 px-4 font-medium">{{ item.service }}</td>
              <td class="py-3 px-4">
                <Badge :class="categoryColors[item.category]">{{ item.category }}</Badge>
              </td>
              <td class="py-3 px-4 text-muted-foreground">{{ item.purpose }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Network Architecture -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Network Architecture</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle class="text-base">Public Subnets</CardTitle>
          </CardHeader>
          <CardContent>
            <ul class="space-y-2 text-sm text-muted-foreground">
              <li>• NAT Gateway for outbound traffic</li>
              <li>• Application Load Balancer</li>
              <li>• Internet Gateway access</li>
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle class="text-base">Private Subnets</CardTitle>
          </CardHeader>
          <CardContent>
            <ul class="space-y-2 text-sm text-muted-foreground">
              <li>• ECS Fargate tasks</li>
              <li>• RDS PostgreSQL instance</li>
              <li>• No direct internet access</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Security -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Security Features</h2>
      <div class="prose prose-slate max-w-none">
        <ul class="space-y-2">
          <li><strong>SSL/TLS Encryption</strong> - All traffic encrypted via CloudFront</li>
          <li><strong>VPC Isolation</strong> - Database in private subnet with no public access</li>
          <li><strong>Secrets Management</strong> - Database credentials stored in AWS Secrets Manager</li>
          <li><strong>JWT Authentication</strong> - Short-lived access tokens with refresh mechanism</li>
          <li><strong>RBAC</strong> - Role-based access control for all API endpoints</li>
          <li><strong>Security Groups</strong> - Strict inbound/outbound rules for all resources</li>
        </ul>
      </div>
    </div>
  </div>
</template>
