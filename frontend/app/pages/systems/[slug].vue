<script setup lang="ts">
import { ArrowLeft, Download, Network, Users, AlertTriangle, Link } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const route = useRoute()
const slug = route.params.slug as string

const { fetchSystem } = useApi()
const { data: system, pending, error } = await fetchSystem(slug)

useHead({
  title: () => system.value ? `${system.value.name} - Resilio` : 'Loading...',
})

const actorTypeColors: Record<string, 'service-user' | 'service-provider' | 'support' | 'regulatory'> = {
  service_user: 'service-user',
  service_provider: 'service-provider',
  support: 'support',
  regulatory: 'regulatory',
}

const qualityColors: Record<string, 'good' | 'stressed' | 'bad' | 'absent'> = {
  good: 'good',
  stressed: 'stressed',
  bad: 'bad',
  absent: 'absent',
}
</script>

<template>
  <div class="container py-8">
    <div v-if="pending" class="flex items-center justify-center py-16">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-goal"></div>
    </div>

    <div v-else-if="error" class="text-center py-16">
      <p class="text-destructive">Failed to load system</p>
      <Button variant="outline" class="mt-4" as-child>
        <NuxtLink to="/systems">
          <ArrowLeft class="mr-2 h-4 w-4" />
          Back to Systems
        </NuxtLink>
      </Button>
    </div>

    <template v-else-if="system">
      <!-- Header -->
      <div class="mb-8">
        <NuxtLink to="/systems" class="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-4">
          <ArrowLeft class="mr-1 h-4 w-4" />
          Back to Systems
        </NuxtLink>

        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-3xl font-bold text-goal-dark">{{ system.name }}</h1>
            <p v-if="system.description" class="text-muted-foreground mt-1 max-w-2xl">
              {{ system.description }}
            </p>
            <div class="flex flex-wrap gap-2 mt-3">
              <Badge variant="default">{{ system.sector_display }}</Badge>
              <Badge v-if="system.subsector" variant="secondary">{{ system.subsector }}</Badge>
              <Badge v-if="system.region" variant="outline">{{ system.region }}</Badge>
              <Badge v-if="system.country" variant="outline">{{ system.country }}</Badge>
            </div>
          </div>
          <Button variant="outline">
            <Download class="mr-2 h-4 w-4" />
            Export DSL
          </Button>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
                <Users class="h-5 w-5 text-goal" />
              </div>
              <div>
                <div class="text-2xl font-bold">{{ system.actors?.length || 0 }}</div>
                <div class="text-sm text-muted-foreground">Actors</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
                <Link class="h-5 w-5 text-goal" />
              </div>
              <div>
                <div class="text-2xl font-bold">{{ system.relationships?.length || 0 }}</div>
                <div class="text-sm text-muted-foreground">Relationships</div>
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
                <div class="text-2xl font-bold">{{ system.risks?.length || 0 }}</div>
                <div class="text-sm text-muted-foreground">Risk Scenarios</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
                <Network class="h-5 w-5 text-goal" />
              </div>
              <div>
                <div class="text-2xl font-bold">v{{ system.version }}</div>
                <div class="text-sm text-muted-foreground">Version</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Actors -->
      <Card class="mb-8">
        <CardHeader>
          <CardTitle class="text-goal-dark">Actors</CardTitle>
        </CardHeader>
        <CardContent>
          <div v-if="!system.actors?.length" class="text-center py-8 text-muted-foreground">
            No actors defined yet
          </div>
          <div v-else class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <div
              v-for="actor in system.actors"
              :key="actor.id"
              class="rounded-lg border p-4 hover:bg-muted/50 transition-colors"
            >
              <div class="flex items-start justify-between mb-2">
                <h4 class="font-medium">{{ actor.name }}</h4>
                <Badge :variant="actorTypeColors[actor.actor_type]">
                  {{ actor.actor_type_display }}
                </Badge>
              </div>
              <p class="text-sm text-muted-foreground line-clamp-2">{{ actor.function }}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Relationships -->
      <Card class="mb-8">
        <CardHeader>
          <CardTitle class="text-goal-dark">Relationships</CardTitle>
        </CardHeader>
        <CardContent>
          <div v-if="!system.relationships?.length" class="text-center py-8 text-muted-foreground">
            No relationships defined yet
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="rel in system.relationships"
              :key="rel.id"
              class="flex items-center justify-between rounded-lg border p-4"
            >
              <div class="flex items-center gap-3">
                <span class="font-medium">{{ rel.from_actor_name }}</span>
                <span class="text-muted-foreground">→</span>
                <span class="font-medium">{{ rel.to_actor_name }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-sm text-muted-foreground">{{ rel.goods_services }}</span>
                <Badge :variant="qualityColors[rel.quality]">
                  {{ rel.quality_display }}
                </Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Risks -->
      <Card>
        <CardHeader>
          <CardTitle class="text-goal-dark">Risk Scenarios</CardTitle>
        </CardHeader>
        <CardContent>
          <div v-if="!system.risks?.length" class="text-center py-8 text-muted-foreground">
            No risks defined yet
          </div>
          <div v-else class="grid gap-4 md:grid-cols-2">
            <div
              v-for="risk in system.risks"
              :key="risk.id"
              class="rounded-lg border p-4"
            >
              <div class="flex items-start justify-between mb-2">
                <h4 class="font-medium">{{ risk.name }}</h4>
                <Badge variant="outline">{{ risk.category_display }}</Badge>
              </div>
              <p v-if="risk.description" class="text-sm text-muted-foreground mb-2">
                {{ risk.description }}
              </p>
              <div class="text-sm">
                <span class="text-muted-foreground">Likelihood:</span>
                <span class="ml-1 font-medium">{{ risk.likelihood_display }}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </template>
  </div>
</template>
