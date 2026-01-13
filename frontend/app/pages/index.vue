<script setup lang="ts">
import { ArrowRight, Network, Shield, Users, Zap } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

useHead({
  title: 'Resilio - R4S Social System Mapping',
  meta: [
    {
      name: 'description',
      content: 'AI-assisted digitalization tool for GOAL Global\'s Resilience for Social Systems (R4S) methodology',
    },
  ],
})

const features = [
  {
    icon: Network,
    title: 'System Mapping',
    description: 'Visualize complex social systems with actors, relationships, and dependencies',
  },
  {
    icon: Users,
    title: 'Actor Assessment',
    description: 'Identify and assess key actors: service users, providers, support, and regulatory',
  },
  {
    icon: Shield,
    title: 'Vulnerability Analysis',
    description: 'Evaluate sensitivity, exposure, and capacity across risk scenarios',
  },
  {
    icon: Zap,
    title: 'AI-Powered',
    description: 'Leverage AI to accelerate system mapping from months to weeks',
  },
]
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="relative overflow-hidden bg-gradient-to-b from-goal/5 to-transparent">
      <div class="container py-24 sm:py-32">
        <div class="mx-auto max-w-3xl text-center">
          <div class="mb-6 inline-flex items-center rounded-full border border-goal/20 bg-goal/10 px-4 py-1.5 text-sm font-medium text-goal">
            GOAL Global Partnership
          </div>
          <h1 class="text-4xl font-bold tracking-tight text-goal-dark sm:text-6xl">
            Resilience for<br />
            <span class="text-goal">Social Systems</span>
          </h1>
          <p class="mt-6 text-lg leading-8 text-muted-foreground">
            AI-assisted digitalization of GOAL's R4S methodology. Map complex social systems,
            assess vulnerabilities, and build resilient communities.
          </p>
          <div class="mt-10 flex items-center justify-center gap-4">
            <Button size="lg" as-child>
              <NuxtLink to="/systems">
                View Systems
                <ArrowRight class="ml-2 h-4 w-4" />
              </NuxtLink>
            </Button>
            <Button variant="outline" size="lg" as-child>
              <NuxtLink to="/about">
                Learn More
              </NuxtLink>
            </Button>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="container py-24">
      <div class="mx-auto max-w-2xl text-center mb-16">
        <h2 class="text-3xl font-bold tracking-tight text-goal-dark sm:text-4xl">
          R4S Methodology
        </h2>
        <p class="mt-4 text-lg text-muted-foreground">
          A comprehensive approach to understanding and strengthening social system resilience
        </p>
      </div>

      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <Card v-for="feature in features" :key="feature.title" class="border-goal/10 hover:border-goal/30 transition-colors">
          <CardHeader>
            <div class="mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-goal/10 text-goal">
              <component :is="feature.icon" class="h-6 w-6" />
            </div>
            <CardTitle class="text-lg text-goal-dark">{{ feature.title }}</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription>{{ feature.description }}</CardDescription>
          </CardContent>
        </Card>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="bg-goal-dark text-white py-16">
      <div class="container">
        <div class="grid grid-cols-1 gap-8 sm:grid-cols-3 text-center">
          <div>
            <div class="text-4xl font-bold text-goal-light">3 weeks</div>
            <div class="mt-2 text-white/70">Target mapping time</div>
            <div class="text-sm text-white/50">(down from 3+ months)</div>
          </div>
          <div>
            <div class="text-4xl font-bold text-goal-light">&lt;€3,000</div>
            <div class="mt-2 text-white/70">Target cost per system</div>
            <div class="text-sm text-white/50">(down from €30,000+)</div>
          </div>
          <div>
            <div class="text-4xl font-bold text-goal-light">4</div>
            <div class="mt-2 text-white/70">Assessment types</div>
            <div class="text-sm text-white/50">Actor, Relationship, Component, Vulnerability</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
