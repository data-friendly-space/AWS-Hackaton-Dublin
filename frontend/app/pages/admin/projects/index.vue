<script setup lang="ts">
import { ArrowLeft, Plus, Search, FolderKanban } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'

useHead({
  title: 'Projects - Admin - Resilio',
})

const { isAuthenticated, isSuperadmin } = useAuth()
const config = useRuntimeConfig()

onMounted(() => {
  if (!isAuthenticated.value || !isSuperadmin.value) {
    navigateTo('/')
  }
})

const searchQuery = ref('')

const { data: projectsData, pending, refresh } = await useFetch<any[]>(
  `${config.public.apiBase}/projects/`,
  {
    headers: {
      Authorization: `Bearer ${useState('auth-access-token').value}`,
    },
  }
)

const projects = computed(() => projectsData.value || [])

const filteredProjects = computed(() => {
  if (!searchQuery.value) return projects.value
  const query = searchQuery.value.toLowerCase()
  return projects.value.filter((project: any) =>
    project.title?.toLowerCase().includes(query) ||
    project.country?.toLowerCase().includes(query) ||
    project.country_area?.toLowerCase().includes(query)
  )
})
</script>

<template>
  <div class="container py-8">
    <div class="flex items-center gap-4 mb-6">
      <Button variant="ghost" size="sm" as-child>
        <NuxtLink to="/admin">
          <ArrowLeft class="h-4 w-4" />
        </NuxtLink>
      </Button>
      <div class="flex-1">
        <h1 class="text-3xl font-bold text-goal-dark">Projects</h1>
        <p class="text-muted-foreground">Manage R4S projects and team assignments</p>
      </div>
      <Button as-child>
        <NuxtLink to="/admin/projects/new">
          <Plus class="mr-2 h-4 w-4" />
          Add Project
        </NuxtLink>
      </Button>
    </div>

    <Card>
      <CardHeader>
        <div class="flex items-center gap-4">
          <div class="relative flex-1">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              v-model="searchQuery"
              placeholder="Search projects..."
              class="pl-10"
            />
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="pending" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-goal"></div>
        </div>
        <div v-else-if="!filteredProjects.length" class="text-center py-8 text-muted-foreground">
          {{ searchQuery ? 'No projects match your search' : 'No projects yet' }}
        </div>
        <div v-else class="space-y-2">
          <NuxtLink
            v-for="project in filteredProjects"
            :key="project.id"
            :to="`/admin/projects/${project.id}`"
            class="flex items-center justify-between p-4 rounded-lg border hover:bg-muted/50 transition-colors"
          >
            <div class="flex items-center gap-4">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10 text-goal">
                <FolderKanban class="h-5 w-5" />
              </div>
              <div>
                <div class="font-medium">{{ project.title }}</div>
                <div class="text-sm text-muted-foreground">
                  {{ project.country }}{{ project.country_area ? ` - ${project.country_area}` : '' }}
                </div>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <div class="text-right text-sm">
                <div>{{ project.manager_count || 0 }} manager{{ project.manager_count !== 1 ? 's' : '' }}</div>
                <div class="text-muted-foreground">{{ project.staff_count || 0 }} staff</div>
              </div>
            </div>
          </NuxtLink>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
