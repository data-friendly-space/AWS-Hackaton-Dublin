<script setup lang="ts">
import { Users, FolderKanban, Shield, Plus } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

useHead({
  title: 'Admin - Resilio',
})

const { isAuthenticated, isSuperadmin, authFetch } = useAuth()
const config = useRuntimeConfig()

// Redirect if not authenticated or not superadmin
onMounted(() => {
  if (!isAuthenticated.value || !isSuperadmin.value) {
    navigateTo('/')
  }
})

// Fetch users
const { data: usersData, pending: usersPending } = await useFetch<{ results: any[] }>(
  `${config.public.apiBase}/users/`,
  {
    headers: {
      Authorization: `Bearer ${useState('auth-access-token').value}`,
    },
  }
)

// Fetch projects
const { data: projectsData, pending: projectsPending } = await useFetch<{ results: any[] }>(
  `${config.public.apiBase}/projects/`,
  {
    headers: {
      Authorization: `Bearer ${useState('auth-access-token').value}`,
    },
  }
)

const users = computed(() => usersData.value?.results || [])
const projects = computed(() => projectsData.value?.results || [])

const usersByRole = computed(() => ({
  superadmin: users.value.filter((u: any) => u.role === 'superadmin').length,
  r4s_manager: users.value.filter((u: any) => u.role === 'r4s_manager').length,
  project_staff: users.value.filter((u: any) => u.role === 'project_staff').length,
}))

const roleColors: Record<string, string> = {
  superadmin: 'default',
  r4s_manager: 'secondary',
  project_staff: 'outline',
}
</script>

<template>
  <div class="container py-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-goal-dark">Admin Dashboard</h1>
        <p class="text-muted-foreground mt-1">Manage users, projects, and system settings</p>
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
              <div class="text-2xl font-bold">{{ users.length }}</div>
              <div class="text-sm text-muted-foreground">Total Users</div>
            </div>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
              <Shield class="h-5 w-5 text-goal" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ usersByRole.superadmin }}</div>
              <div class="text-sm text-muted-foreground">Superadmins</div>
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
              <div class="text-2xl font-bold">{{ usersByRole.r4s_manager }}</div>
              <div class="text-sm text-muted-foreground">R4S Managers</div>
            </div>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
              <FolderKanban class="h-5 w-5 text-goal" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ projects.length }}</div>
              <div class="text-sm text-muted-foreground">Projects</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <!-- Users Section -->
      <Card>
        <CardHeader>
          <div class="flex items-center justify-between">
            <div>
              <CardTitle>Users</CardTitle>
              <CardDescription>Manage system users</CardDescription>
            </div>
            <Button size="sm" as-child>
              <NuxtLink to="/admin/users/new">
                <Plus class="mr-2 h-4 w-4" />
                Add User
              </NuxtLink>
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="usersPending" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-goal"></div>
          </div>
          <div v-else-if="!users.length" class="text-center py-8 text-muted-foreground">
            No users yet
          </div>
          <div v-else class="space-y-3">
            <NuxtLink
              v-for="user in users.slice(0, 5)"
              :key="user.id"
              :to="`/admin/users/${user.id}`"
              class="flex items-center justify-between p-3 rounded-lg border hover:bg-muted/50 transition-colors"
            >
              <div>
                <div class="font-medium">{{ user.full_name }}</div>
                <div class="text-sm text-muted-foreground">{{ user.email }}</div>
              </div>
              <Badge :variant="roleColors[user.role] as any">{{ user.role_display }}</Badge>
            </NuxtLink>
            <Button v-if="users.length > 5" variant="outline" class="w-full" as-child>
              <NuxtLink to="/admin/users">View all {{ users.length }} users</NuxtLink>
            </Button>
          </div>
        </CardContent>
      </Card>

      <!-- Projects Section -->
      <Card>
        <CardHeader>
          <div class="flex items-center justify-between">
            <div>
              <CardTitle>Projects</CardTitle>
              <CardDescription>Manage R4S projects</CardDescription>
            </div>
            <Button size="sm" as-child>
              <NuxtLink to="/admin/projects/new">
                <Plus class="mr-2 h-4 w-4" />
                Add Project
              </NuxtLink>
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="projectsPending" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-goal"></div>
          </div>
          <div v-else-if="!projects.length" class="text-center py-8 text-muted-foreground">
            No projects yet
          </div>
          <div v-else class="space-y-3">
            <NuxtLink
              v-for="project in projects.slice(0, 5)"
              :key="project.id"
              :to="`/admin/projects/${project.id}`"
              class="flex items-center justify-between p-3 rounded-lg border hover:bg-muted/50 transition-colors"
            >
              <div>
                <div class="font-medium">{{ project.title }}</div>
                <div class="text-sm text-muted-foreground">{{ project.country }} {{ project.country_area ? `- ${project.country_area}` : '' }}</div>
              </div>
              <div class="text-sm text-muted-foreground">
                {{ project.manager_count }} managers, {{ project.staff_count }} staff
              </div>
            </NuxtLink>
            <Button v-if="projects.length > 5" variant="outline" class="w-full" as-child>
              <NuxtLink to="/admin/projects">View all {{ projects.length }} projects</NuxtLink>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
