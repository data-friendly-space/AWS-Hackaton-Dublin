<script setup lang="ts">
import { ExternalLink, Check } from 'lucide-vue-next'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

useHead({
  title: 'About - Resilio',
})

const assessmentTypes = [
  {
    name: 'Actor Assessment',
    description: 'Identify key actors in the social system, their functions, needs, and concerns',
    steps: [
      'Identify service users, providers, support, and regulatory actors',
      'Document each actor\'s function within the system',
      'Record their needs and worries',
    ],
  },
  {
    name: 'Relationship Assessment',
    description: 'Map the flows of goods, services, and resources between actors',
    steps: [
      'Identify input and output relationships',
      'Document goods, services, and resources exchanged',
      'Assess relationship quality (good, stressed, bad, absent)',
    ],
  },
  {
    name: 'Component Assessment',
    description: 'Evaluate actor importance through production and replaceability',
    steps: [
      'Score production/throughput level (1-5)',
      'Score replaceability (1-5, where 5 = not replaceable)',
      'Calculate relevance score (production × replaceability)',
    ],
  },
  {
    name: 'Vulnerability Assessment',
    description: 'Analyze how risk scenarios affect system actors',
    steps: [
      'Score sensitivity to each risk (1-5)',
      'Score exposure likelihood (1-5)',
      'Score adaptive capacity (1-5)',
      'Calculate vulnerability: (sensitivity + exposure) / capacity',
    ],
  },
]
</script>

<template>
  <div>
    <!-- Hero -->
    <section class="bg-goal-dark text-white py-16">
      <div class="container">
        <div class="max-w-3xl">
          <h1 class="text-4xl font-bold mb-4">About Resilio</h1>
          <p class="text-xl text-white/80">
            AI-assisted digitalization of GOAL Global's Resilience for Social Systems (R4S) methodology
          </p>
        </div>
      </div>
    </section>

    <!-- Mission -->
    <section class="container py-16">
      <div class="max-w-3xl">
        <h2 class="text-2xl font-bold text-goal-dark mb-4">Our Mission</h2>
        <p class="text-muted-foreground mb-4">
          Resilio aims to dramatically reduce the time and cost of social system mapping while
          maintaining the analytical rigor of the R4S methodology. By leveraging AI, we can help
          humanitarian organizations understand and strengthen community resilience at scale.
        </p>
        <div class="grid sm:grid-cols-2 gap-6 mt-8">
          <Card>
            <CardHeader>
              <CardTitle class="text-goal">Time Reduction</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="text-3xl font-bold text-goal-dark mb-2">3+ months → &lt;3 weeks</div>
              <CardDescription>Target time for complete system mapping</CardDescription>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle class="text-goal">Cost Reduction</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="text-3xl font-bold text-goal-dark mb-2">€30,000+ → &lt;€3,000</div>
              <CardDescription>Target cost per system assessment</CardDescription>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>

    <!-- R4S Methodology -->
    <section class="bg-gray-200 py-16">
      <div class="container">
        <h2 class="text-2xl font-bold text-goal-dark mb-8">R4S Methodology</h2>
        <div class="grid gap-6 md:grid-cols-2">
          <Card v-for="assessment in assessmentTypes" :key="assessment.name">
            <CardHeader>
              <CardTitle class="text-lg text-goal-dark">{{ assessment.name }}</CardTitle>
              <CardDescription>{{ assessment.description }}</CardDescription>
            </CardHeader>
            <CardContent>
              <ul class="space-y-2">
                <li v-for="step in assessment.steps" :key="step" class="flex items-start gap-2">
                  <Check class="h-4 w-4 text-goal mt-0.5 shrink-0" />
                  <span class="text-sm">{{ step }}</span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>

    <!-- GOAL Partnership -->
    <section class="container py-16">
      <div class="max-w-3xl">
        <h2 class="text-2xl font-bold text-goal-dark mb-4">GOAL Global Partnership</h2>
        <p class="text-muted-foreground mb-4">
          Resilio is built in partnership with GOAL Global, implementing their proven R4S (Resilience
          for Social Systems) methodology. GOAL is an international humanitarian organization that
          has been responding to humanitarian crises since 1977.
        </p>
        <a
          href="https://www.goalglobal.org"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center text-goal hover:text-goal-dark transition-colors"
        >
          Learn more about GOAL Global
          <ExternalLink class="ml-1 h-4 w-4" />
        </a>
      </div>
    </section>
  </div>
</template>
