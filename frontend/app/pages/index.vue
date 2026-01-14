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
      <div class="container py-16 sm:py-24">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <div class="mb-6 inline-flex items-center rounded-full border border-goal/20 bg-goal/10 px-4 py-1.5 text-sm font-medium text-goal">
              GOAL Global Partnership
            </div>
            <h1 class="text-4xl font-bold tracking-tight text-goal-dark sm:text-5xl lg:text-6xl">
              Resilience for<br />
              <span class="text-goal">Social Systems</span>
            </h1>
            <p class="mt-6 text-lg leading-8 text-muted-foreground max-w-xl">
              AI-assisted digitalization of GOAL's R4S methodology. Map complex social systems,
              assess vulnerabilities, and build resilient communities.
            </p>
            <div class="mt-10 flex items-center gap-4">
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
          <div class="relative hidden lg:block">
            <div class="absolute -top-4 -right-4 w-72 h-72 bg-goal/10 rounded-full blur-3xl" />
            <div class="absolute -bottom-8 -left-8 w-64 h-64 bg-goal-light/10 rounded-full blur-3xl" />
            <img
              src="/logo.svg"
              alt="Resilio Logo"
              class="relative w-64 h-64 mx-auto drop-shadow-xl"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- System Diagram Preview -->
    <section class="container py-16">
      <div class="mx-auto max-w-2xl text-center mb-12">
        <h2 class="text-3xl font-bold tracking-tight text-goal-dark sm:text-4xl">
          Interactive System Mapping
        </h2>
        <p class="mt-4 text-lg text-muted-foreground">
          Visualize actors, relationships, and system dependencies in an intuitive interface
        </p>
      </div>

      <div class="relative rounded-2xl border-2 border-gray-300 bg-white shadow-xl overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-10 bg-muted/50 flex items-center px-4 gap-2">
          <div class="w-3 h-3 rounded-full bg-red-400" />
          <div class="w-3 h-3 rounded-full bg-yellow-400" />
          <div class="w-3 h-3 rounded-full bg-green-400" />
          <span class="ml-4 text-xs text-muted-foreground font-medium">RMNCAH Health System - Eastern Region</span>
        </div>
        <div class="pt-10">
          <img
            src="/images/system-diagram.svg"
            alt="System Diagram Example"
            class="w-full"
          />
        </div>
      </div>

      <div class="mt-8 text-center">
        <Button variant="outline" as-child>
          <NuxtLink to="/systems">
            Explore Systems
            <ArrowRight class="ml-2 h-4 w-4" />
          </NuxtLink>
        </Button>
      </div>
    </section>

    <!-- Features Section -->
    <section class="bg-gray-200 py-24">
      <div class="container">
        <div class="mx-auto max-w-2xl text-center mb-16">
          <h2 class="text-3xl font-bold tracking-tight text-goal-dark sm:text-4xl">
            R4S Methodology
          </h2>
          <p class="mt-4 text-lg text-muted-foreground">
            A comprehensive approach to understanding and strengthening social system resilience
          </p>
        </div>

        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <Card v-for="feature in features" :key="feature.title" class="bg-white border-goal/10 hover:border-goal/30 hover:shadow-lg transition-all">
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
      </div>
    </section>

    <!-- Stats Section -->
    <section class="bg-goal-dark text-white py-20">
      <div class="container">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold">Transforming Humanitarian Response</h2>
          <p class="mt-2 text-white/70">Dramatically reducing the time and cost of social system mapping</p>
        </div>
        <div class="grid grid-cols-1 gap-8 sm:grid-cols-3 text-center">
          <div class="p-6 rounded-xl bg-white/5">
            <div class="text-5xl font-bold text-goal-light">3 weeks</div>
            <div class="mt-3 text-lg text-white/90">Target mapping time</div>
            <div class="text-sm text-white/50">(down from 3+ months)</div>
          </div>
          <div class="p-6 rounded-xl bg-white/5">
            <div class="text-5xl font-bold text-goal-light">&lt;€3,000</div>
            <div class="mt-3 text-lg text-white/90">Target cost per system</div>
            <div class="text-sm text-white/50">(down from €30,000+)</div>
          </div>
          <div class="p-6 rounded-xl bg-white/5">
            <div class="text-5xl font-bold text-goal-light">4</div>
            <div class="mt-3 text-lg text-white/90">Assessment types</div>
            <div class="text-sm text-white/50">Actor, Relationship, Component, Vulnerability</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="container py-24">
      <div class="relative rounded-3xl bg-gradient-to-r from-goal to-goal-light p-12 text-center text-white overflow-hidden">
        <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
        <div class="absolute bottom-0 left-0 w-48 h-48 bg-white/10 rounded-full blur-3xl" />
        <div class="relative">
          <h2 class="text-3xl font-bold sm:text-4xl">Ready to map your social system?</h2>
          <p class="mt-4 text-lg text-white/80 max-w-2xl mx-auto">
            Get started with Resilio and transform how your organization understands and strengthens community resilience.
          </p>
          <div class="mt-8 flex items-center justify-center gap-4">
            <Button size="lg" variant="secondary" as-child>
              <NuxtLink to="/login">
                Get Started
                <ArrowRight class="ml-2 h-4 w-4" />
              </NuxtLink>
            </Button>
            <Button size="lg" variant="outline" class="border-white/30 text-white hover:bg-white/10" as-child>
              <NuxtLink to="/about">
                Learn More
              </NuxtLink>
            </Button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
