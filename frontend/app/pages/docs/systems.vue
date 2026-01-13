<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'Systems & Actors - Documentation - Resilio',
})

const actorTypes = [
  {
    type: 'Service User',
    color: 'bg-blue-100 text-blue-700 border-blue-300',
    description: 'Primary beneficiaries of the social system. These are the individuals or groups that receive services.',
    examples: ['Pregnant women', 'Children under 5', 'Farmers', 'Students']
  },
  {
    type: 'Service Provider',
    color: 'bg-green-100 text-green-700 border-green-300',
    description: 'Organizations or individuals that deliver services to users. They form the backbone of service delivery.',
    examples: ['Health centers', 'Schools', 'NGOs', 'Community health workers']
  },
  {
    type: 'Support',
    color: 'bg-purple-100 text-purple-700 border-purple-300',
    description: 'Entities that enable service providers to function. They provide resources, training, or coordination.',
    examples: ['UNICEF', 'World Bank', 'Training institutions', 'Suppliers']
  },
  {
    type: 'Regulatory',
    color: 'bg-orange-100 text-orange-700 border-orange-300',
    description: 'Government bodies and institutions that set policies, standards, and provide oversight.',
    examples: ['Ministry of Health', 'Local government', 'Regulatory bodies']
  }
]

const qualityLevels = [
  { level: 'Good', color: 'bg-green-500', description: 'Relationship is functioning well with consistent, reliable service delivery' },
  { level: 'Stressed', color: 'bg-amber-500', description: 'Relationship is under pressure but still functioning' },
  { level: 'Bad', color: 'bg-red-500', description: 'Relationship is severely impaired or intermittent' },
  { level: 'Absent', color: 'bg-gray-400', description: 'No functional relationship exists' }
]

const sectors = [
  'Health', 'Education', 'Market', 'Water', 'Protection', 'Nutrition', 'Shelter', 'Livelihoods'
]
</script>

<template>
  <div>
    <Badge class="mb-4">Core Concepts</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">Systems & Actors</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Understanding the R4S framework for mapping social systems.
    </p>

    <!-- What is a System -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">What is a Social System?</h2>
      <div class="prose prose-slate max-w-none">
        <p>
          In the R4S methodology, a <strong>social system</strong> is a network of actors and their relationships
          that work together to deliver essential services to a population. Systems are defined by:
        </p>
        <ul>
          <li><strong>Sector</strong> - The domain (health, education, water, etc.)</li>
          <li><strong>Geography</strong> - The region and country</li>
          <li><strong>Service Users</strong> - The target beneficiaries</li>
          <li><strong>Service Flow</strong> - How services reach users</li>
        </ul>
      </div>
    </div>

    <!-- Sectors -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Supported Sectors</h2>
      <div class="flex flex-wrap gap-2">
        <Badge v-for="sector in sectors" :key="sector" variant="outline" class="text-base py-1.5 px-3">
          {{ sector }}
        </Badge>
      </div>
    </div>

    <!-- Actor Types -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Actor Types</h2>
      <p class="text-muted-foreground mb-6">
        Every system is composed of four types of actors, each playing a distinct role in the service delivery chain.
      </p>
      <div class="grid gap-4">
        <Card v-for="actor in actorTypes" :key="actor.type" :class="['border-2', actor.color.split(' ')[2]]">
          <CardHeader>
            <CardTitle class="flex items-center gap-3">
              <Badge :class="actor.color">{{ actor.type }}</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p class="text-muted-foreground mb-3">{{ actor.description }}</p>
            <div class="flex flex-wrap gap-2">
              <span class="text-sm text-muted-foreground">Examples:</span>
              <Badge v-for="example in actor.examples" :key="example" variant="secondary" class="text-xs">
                {{ example }}
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Relationships -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Relationships</h2>
      <p class="text-muted-foreground mb-6">
        Relationships describe how actors interact and exchange goods, services, or information.
        Each relationship has a quality assessment.
      </p>

      <Card class="mb-6">
        <CardHeader>
          <CardTitle>Relationship Properties</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div>
              <h4 class="font-medium mb-1">From Actor → To Actor</h4>
              <p class="text-sm text-muted-foreground">The direction of the service or goods flow</p>
            </div>
            <div>
              <h4 class="font-medium mb-1">Goods/Services</h4>
              <p class="text-sm text-muted-foreground">What is exchanged (e.g., "Medical supplies", "Training", "Funding")</p>
            </div>
            <div>
              <h4 class="font-medium mb-1">Quality</h4>
              <p class="text-sm text-muted-foreground">Current state of the relationship</p>
            </div>
            <div>
              <h4 class="font-medium mb-1">Criticality</h4>
              <p class="text-sm text-muted-foreground">How important this relationship is to system function</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <h3 class="text-lg font-semibold mb-4">Quality Levels</h3>
      <div class="grid gap-3 md:grid-cols-2">
        <div v-for="quality in qualityLevels" :key="quality.level" class="flex items-start gap-3 p-3 rounded-lg border">
          <div :class="['w-4 h-4 rounded-full shrink-0 mt-0.5', quality.color]"></div>
          <div>
            <h4 class="font-medium">{{ quality.level }}</h4>
            <p class="text-sm text-muted-foreground">{{ quality.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Components -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">System Components</h2>
      <p class="text-muted-foreground mb-6">
        Components are the building blocks that enable the system to function.
      </p>
      <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardContent class="pt-6">
            <Badge class="bg-slate-100 text-slate-700 mb-2">Infrastructure</Badge>
            <p class="text-sm text-muted-foreground">Physical assets like buildings, equipment, roads, power supply</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <Badge class="bg-blue-100 text-blue-700 mb-2">Human Resource</Badge>
            <p class="text-sm text-muted-foreground">Staff, volunteers, trained personnel capacity</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <Badge class="bg-emerald-100 text-emerald-700 mb-2">Financial</Badge>
            <p class="text-sm text-muted-foreground">Funding sources, budgets, financial mechanisms</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <Badge class="bg-cyan-100 text-cyan-700 mb-2">Information</Badge>
            <p class="text-sm text-muted-foreground">Data systems, communication channels, reporting</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <Badge class="bg-violet-100 text-violet-700 mb-2">Governance</Badge>
            <p class="text-sm text-muted-foreground">Policies, coordination mechanisms, leadership</p>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Risks -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Risk Scenarios</h2>
      <p class="text-muted-foreground mb-6">
        Risk scenarios document potential threats to system function, including their likelihood and impact.
      </p>
      <div class="prose prose-slate max-w-none">
        <h4>Risk Categories</h4>
        <ul>
          <li><strong>Climate</strong> - Droughts, floods, extreme weather</li>
          <li><strong>Conflict</strong> - Violence, displacement, instability</li>
          <li><strong>Economic</strong> - Market shocks, inflation, supply chain disruption</li>
          <li><strong>Health</strong> - Disease outbreaks, pandemics</li>
          <li><strong>Political</strong> - Policy changes, funding cuts, governance failures</li>
        </ul>
      </div>
    </div>
  </div>
</template>
