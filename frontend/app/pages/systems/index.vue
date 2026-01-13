<script setup lang="ts">
import { MapPin, Calendar, Users, AlertTriangle, Plus } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

useHead({
  title: 'Systems - Resilio',
})

const { fetchSystems } = useApi()
const { data, pending, error } = await fetchSystems()

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

    <div v-if="pending" class="flex items-center justify-center py-16">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-goal"></div>
    </div>

    <div v-else-if="error" class="text-center py-16">
      <p class="text-destructive">Failed to load systems. Make sure the backend is running.</p>
      <p class="text-sm text-muted-foreground mt-2">{{ error.message }}</p>
    </div>

    <div v-else-if="!data?.results?.length" class="text-center py-16">
      <div class="mx-auto h-16 w-16 rounded-full bg-goal/10 flex items-center justify-center mb-4">
        <Users class="h-8 w-8 text-goal" />
      </div>
      <h3 class="text-lg font-medium text-goal-dark">No systems yet</h3>
      <p class="text-muted-foreground mt-1">Get started by creating your first system</p>
      <Button class="mt-4">
        <Plus class="mr-2 h-4 w-4" />
        Create System
      </Button>
    </div>

    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <NuxtLink
        v-for="system in data.results"
        :key="system.id"
        :to="`/systems/${system.slug}`"
        class="block"
      >
        <Card class="h-full hover:border-goal/30 transition-colors cursor-pointer">
          <CardHeader>
            <div class="flex items-start justify-between">
              <div>
                <CardTitle class="text-lg text-goal-dark">{{ system.name }}</CardTitle>
                <CardDescription class="mt-1">
                  {{ system.description || 'No description' }}
                </CardDescription>
              </div>
              <Badge :class="sectorColors[system.sector] || 'bg-gray-100 text-gray-700'">
                {{ system.sector_display }}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
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
            <div v-if="system.assessment_date" class="mt-3 flex items-center gap-1 text-sm text-muted-foreground">
              <Calendar class="h-4 w-4" />
              Assessed: {{ new Date(system.assessment_date).toLocaleDateString() }}
            </div>
          </CardContent>
        </Card>
      </NuxtLink>
    </div>
  </div>
</template>
