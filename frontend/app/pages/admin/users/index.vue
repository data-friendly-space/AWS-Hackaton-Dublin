<script setup lang="ts">
import { ArrowLeft, Plus, Search, UserCog } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'

useHead({
  title: 'Users - Admin - Resilio',
})

const { isAuthenticated, isSuperadmin } = useAuth()
const config = useRuntimeConfig()

onMounted(() => {
  if (!isAuthenticated.value || !isSuperadmin.value) {
    navigateTo('/')
  }
})

const searchQuery = ref('')

const { data: usersData, pending, refresh } = await useFetch<any[]>(
  `${config.public.apiBase}/users/`,
  {
    headers: {
      Authorization: `Bearer ${useState('auth-access-token').value}`,
    },
  }
)

const users = computed(() => usersData.value || [])

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const query = searchQuery.value.toLowerCase()
  return users.value.filter((user: any) =>
    user.full_name?.toLowerCase().includes(query) ||
    user.email?.toLowerCase().includes(query) ||
    user.role_display?.toLowerCase().includes(query)
  )
})

const roleColors: Record<string, string> = {
  superadmin: 'default',
  r4s_manager: 'secondary',
  project_staff: 'outline',
}
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
        <h1 class="text-3xl font-bold text-goal-dark">Users</h1>
        <p class="text-muted-foreground">Manage system users and their roles</p>
      </div>
      <Button as-child>
        <NuxtLink to="/admin/users/new">
          <Plus class="mr-2 h-4 w-4" />
          Add User
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
              placeholder="Search users..."
              class="pl-10"
            />
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="pending" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-goal"></div>
        </div>
        <div v-else-if="!filteredUsers.length" class="text-center py-8 text-muted-foreground">
          {{ searchQuery ? 'No users match your search' : 'No users yet' }}
        </div>
        <div v-else class="space-y-2">
          <NuxtLink
            v-for="user in filteredUsers"
            :key="user.id"
            :to="`/admin/users/${user.id}`"
            class="flex items-center justify-between p-4 rounded-lg border hover:bg-muted/50 transition-colors"
          >
            <div class="flex items-center gap-4">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-goal/10 text-goal font-semibold">
                {{ user.first_name?.charAt(0) || user.email?.charAt(0) }}{{ user.last_name?.charAt(0) || '' }}
              </div>
              <div>
                <div class="font-medium">{{ user.full_name || user.email }}</div>
                <div class="text-sm text-muted-foreground">{{ user.email }}</div>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <div class="text-sm text-muted-foreground hidden sm:block">
                {{ user.department || 'No department' }}
              </div>
              <Badge :variant="roleColors[user.role] as any">{{ user.role_display }}</Badge>
              <div
                class="h-2 w-2 rounded-full"
                :class="user.is_active ? 'bg-green-500' : 'bg-red-500'"
                :title="user.is_active ? 'Active' : 'Inactive'"
              />
            </div>
          </NuxtLink>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
