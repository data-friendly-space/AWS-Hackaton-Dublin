<script setup lang="ts">
import { MapPin, Calendar, Users, AlertTriangle, Plus, Network, TrendingUp, TrendingDown, Component } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'

useHead({
  title: 'Systems - Resilio',
})

const { getAllSystems } = useMockSystems()
const systems = getAllSystems()

const sectorColors: Record<string, string> = {
  health: 'bg-red-100 text-red-700',
  education: 'bg-blue-100 text-blue-700',
  market: 'bg-amber-100 text-amber-700',
  water: 'bg-cyan-100 text-cyan-700',
  protection: 'bg-purple-100 text-purple-700',
  nutrition: 'bg-green-100 text-green-700',
  shelter: 'bg-orange-100 text-orange-700',
  livelihoods: 'bg-emerald-100 text-emerald-700',
}

function getResilienceColor(score: number): string {
  if (score >= 70) return 'text-green-600'
  if (score >= 50) return 'text-amber-600'
  return 'text-red-600'
}

function getResilienceLabel(score: number): string {
  if (score >= 70) return 'Strong'
  if (score >= 50) return 'Moderate'
  return 'Weak'
}
</script>

<template>
  <div class="container py-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-goal-dark">Systems</h1>
        <p class="text-muted-foreground mt-1">
          Social systems mapped using the R4S methodology
        </p>
      </div>
      <Button>
        <Plus class="mr-2 h-4 w-4" />
        New System
      </Button>
    </div>

    <!-- Stats Overview -->
    <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-8">
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
              <Network class="h-5 w-5 text-goal" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ systems.length }}</div>
              <div class="text-sm text-muted-foreground">Total Systems</div>
            </div>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
              <Users class="h-5 w-5 text-goal" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ systems.reduce((sum, s) => sum + s.actor_count, 0) }}</div>
              <div class="text-sm text-muted-foreground">Total Actors</div>
            </div>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
              <Component class="h-5 w-5 text-goal" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ systems.reduce((sum, s) => sum + s.component_count, 0) }}</div>
              <div class="text-sm text-muted-foreground">Components</div>
            </div>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
              <AlertTriangle class="h-5 w-5 text-goal" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ systems.reduce((sum, s) => sum + s.risk_count, 0) }}</div>
              <div class="text-sm text-muted-foreground">Risk Scenarios</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Systems Grid -->
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <NuxtLink
        v-for="system in systems"
        :key="system.id"
        :to="`/systems/${system.slug}`"
        class="block"
      >
        <Card class="h-full hover:border-goal/30 hover:shadow-lg transition-all cursor-pointer">
          <CardHeader class="pb-3">
            <div class="flex items-start justify-between">
              <div class="flex-1 min-w-0">
                <CardTitle class="text-lg text-goal-dark truncate">{{ system.name }}</CardTitle>
                <CardDescription class="mt-1 line-clamp-2">
                  {{ system.description }}
                </CardDescription>
              </div>
              <Badge :class="sectorColors[system.sector] || 'bg-gray-100 text-gray-700'" class="ml-2 shrink-0">
                {{ system.sector_display }}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <!-- Resilience Score -->
            <div class="mb-4">
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm text-muted-foreground">Resilience Score</span>
                <span :class="['text-sm font-medium', getResilienceColor(system.resilience_score)]">
                  {{ system.resilience_score }}% - {{ getResilienceLabel(system.resilience_score) }}
                </span>
              </div>
              <Progress :model-value="system.resilience_score" class="h-2" />
            </div>

            <!-- Stats Row -->
            <div class="flex flex-wrap gap-4 text-sm text-muted-foreground">
              <div v-if="system.region || system.country" class="flex items-center gap-1">
                <MapPin class="h-4 w-4" />
                {{ system.region || system.country }}
              </div>
              <div class="flex items-center gap-1">
                <Users class="h-4 w-4" />
                {{ system.actor_count }} actors
              </div>
              <div class="flex items-center gap-1">
                <AlertTriangle class="h-4 w-4" />
                {{ system.risk_count }} risks
              </div>
            </div>

            <!-- Assessment Date -->
            <div v-if="system.assessment_date" class="mt-3 flex items-center gap-1 text-sm text-muted-foreground">
              <Calendar class="h-4 w-4" />
              Assessed: {{ new Date(system.assessment_date).toLocaleDateString() }}
            </div>

            <!-- Version Badge -->
            <div class="mt-3 flex items-center gap-2">
              <Badge variant="outline" class="text-xs">v{{ system.version }}</Badge>
              <Badge v-if="system.subsector" variant="secondary" class="text-xs">{{ system.subsector }}</Badge>
            </div>
          </CardContent>
        </Card>
      </NuxtLink>
    </div>
  </div>
</template>
