<script setup lang="ts">
import { ArrowRight, Network, Shield, Users, Zap, Clock, DollarSign, Target } from 'lucide-vue-next'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'Documentation - Resilio',
})

const features = [
  {
    icon: Network,
    title: 'System Mapping',
    description: 'Visualize complex social systems with actors, relationships, and dependencies'
  },
  {
    icon: Users,
    title: 'Actor Assessment',
    description: 'Identify service users, providers, support, and regulatory actors'
  },
  {
    icon: Shield,
    title: 'Vulnerability Analysis',
    description: 'Evaluate sensitivity, exposure, and capacity across risk scenarios'
  },
  {
    icon: Zap,
    title: 'AI-Powered',
    description: 'Claude Opus 4.5 via Amazon Bedrock for intelligent analysis'
  }
]

const metrics = [
  { icon: Clock, label: 'Mapping Time', value: '3 weeks', subtext: 'down from 3+ months' },
  { icon: DollarSign, label: 'Cost per System', value: '<€3,000', subtext: 'down from €30,000+' },
  { icon: Target, label: 'Assessment Types', value: '4', subtext: 'Actor, Relationship, Component, Risk' }
]
</script>

<template>
  <div>
    <!-- Hero -->
    <div class="mb-12">
      <Badge class="mb-4">Documentation</Badge>
      <h1 class="text-4xl font-bold text-goal-dark mb-4">
        Resilio Platform Documentation
      </h1>
      <p class="text-xl text-muted-foreground max-w-2xl">
        An AI-assisted digitalization tool for GOAL Global's Resilience for Social Systems (R4S) methodology.
        Dramatically reduce the time and cost of social system mapping.
      </p>
    </div>

    <!-- Quick Links -->
    <div class="grid gap-4 md:grid-cols-2 mb-12">
      <NuxtLink to="/docs/quickstart">
        <Card class="h-full hover:border-goal/30 hover:shadow-md transition-all cursor-pointer">
          <CardHeader>
            <CardTitle class="flex items-center gap-2 text-goal-dark">
              <Zap class="h-5 w-5 text-goal" />
              Quick Start Guide
            </CardTitle>
            <CardDescription>
              Get up and running with Resilio in minutes
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button variant="link" class="p-0 h-auto">
              Get started <ArrowRight class="ml-1 h-4 w-4" />
            </Button>
          </CardContent>
        </Card>
      </NuxtLink>

      <NuxtLink to="/docs/api">
        <Card class="h-full hover:border-goal/30 hover:shadow-md transition-all cursor-pointer">
          <CardHeader>
            <CardTitle class="flex items-center gap-2 text-goal-dark">
              <Network class="h-5 w-5 text-goal" />
              API Reference
            </CardTitle>
            <CardDescription>
              Complete REST API documentation with examples
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button variant="link" class="p-0 h-auto">
              View API docs <ArrowRight class="ml-1 h-4 w-4" />
            </Button>
          </CardContent>
        </Card>
      </NuxtLink>
    </div>

    <!-- Target Metrics -->
    <div class="mb-12">
      <h2 class="text-2xl font-bold text-goal-dark mb-6">Target Metrics</h2>
      <div class="grid gap-4 md:grid-cols-3">
        <Card v-for="metric in metrics" :key="metric.label" class="bg-goal-dark text-white">
          <CardContent class="pt-6">
            <component :is="metric.icon" class="h-8 w-8 text-goal-light mb-3" />
            <div class="text-3xl font-bold">{{ metric.value }}</div>
            <div class="text-white/90">{{ metric.label }}</div>
            <div class="text-sm text-white/60 mt-1">{{ metric.subtext }}</div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Features -->
    <div class="mb-12">
      <h2 class="text-2xl font-bold text-goal-dark mb-6">Key Features</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <Card v-for="feature in features" :key="feature.title">
          <CardContent class="pt-6">
            <div class="flex items-start gap-4">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10 shrink-0">
                <component :is="feature.icon" class="h-5 w-5 text-goal" />
              </div>
              <div>
                <h3 class="font-semibold text-goal-dark">{{ feature.title }}</h3>
                <p class="text-sm text-muted-foreground mt-1">{{ feature.description }}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- What's in this documentation -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-6">What's in this Documentation</h2>
      <div class="prose prose-slate max-w-none">
        <ul class="space-y-3">
          <li>
            <strong>Getting Started</strong> - Overview, architecture, and quick start guide
          </li>
          <li>
            <strong>Core Concepts</strong> - Systems, actors, relationships, and data models
          </li>
          <li>
            <strong>API Reference</strong> - Complete REST API documentation with request/response examples
          </li>
          <li>
            <strong>Deployment</strong> - AWS infrastructure setup and configuration
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
