<script setup lang="ts">
import { ArrowLeft, Trash2, UserPlus, X, Users } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'

const route = useRoute()
const projectId = route.params.id

useHead({
  title: 'Edit Project - Admin - Resilio',
})

const { isAuthenticated, isSuperadmin } = useAuth()
const config = useRuntimeConfig()

onMounted(() => {
  if (!isAuthenticated.value || !isSuperadmin.value) {
    navigateTo('/')
  }
})

// Fetch project
const { data: projectData, pending, refresh: refreshProject } = await useFetch<any>(
  `${config.public.apiBase}/projects/${projectId}/`,
  {
    headers: {
      Authorization: `Bearer ${useState('auth-access-token').value}`,
    },
  }
)

// Fetch project members
const { data: membersData, refresh: refreshMembers } = await useFetch<any[]>(
  `${config.public.apiBase}/projects/${projectId}/members/`,
  {
    headers: {
      Authorization: `Bearer ${useState('auth-access-token').value}`,
    },
  }
)

// Fetch available users (R4S Managers and Project Staff)
const { data: managersData } = await useFetch<any[]>(
  `${config.public.apiBase}/users/managers/`,
  {
    headers: {
      Authorization: `Bearer ${useState('auth-access-token').value}`,
    },
  }
)

const { data: staffData } = await useFetch<any[]>(
  `${config.public.apiBase}/users/staff/`,
  {
    headers: {
      Authorization: `Bearer ${useState('auth-access-token').value}`,
    },
  }
)

const form = reactive({
  title: '',
  country: '',
  country_area: '',
  description: '',
})

watch(projectData, (project) => {
  if (project) {
    form.title = project.title || ''
    form.country = project.country || ''
    form.country_area = project.country_area || ''
    form.description = project.description || ''
  }
}, { immediate: true })

const members = computed(() => membersData.value || [])
const managers = computed(() => managersData.value || [])
const staff = computed(() => staffData.value || [])

const projectManagers = computed(() => members.value.filter((m: any) => m.role === 'manager'))
const projectStaff = computed(() => members.value.filter((m: any) => m.role === 'staff'))

// Available users (not already assigned)
const availableManagers = computed(() => {
  const assignedIds = new Set(members.value.map((m: any) => m.user?.id))
  return managers.value.filter((u: any) => !assignedIds.has(u.id))
})

const availableStaff = computed(() => {
  const assignedIds = new Set(members.value.map((m: any) => m.user?.id))
  return staff.value.filter((u: any) => !assignedIds.has(u.id))
})

const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    await $fetch(`${config.public.apiBase}/projects/${projectId}/`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${useState('auth-access-token').value}`,
      },
      body: form,
    })

    success.value = 'Project updated successfully'
    await refreshProject()
  } catch (e: any) {
    error.value = e?.data?.detail || 'Failed to update project'
  } finally {
    loading.value = false
  }
}

// Team management
const showAddManager = ref(false)
const showAddStaff = ref(false)
const selectedUserId = ref('')
const addingMember = ref(false)

async function addManager() {
  if (!selectedUserId.value) return
  addingMember.value = true

  try {
    await $fetch(`${config.public.apiBase}/projects/${projectId}/assign_manager/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${useState('auth-access-token').value}`,
      },
      body: { user_id: selectedUserId.value },
    })

    await refreshMembers()
    showAddManager.value = false
    selectedUserId.value = ''
  } catch (e: any) {
    error.value = e?.data?.error || 'Failed to add manager'
  } finally {
    addingMember.value = false
  }
}

async function addStaffMember() {
  if (!selectedUserId.value) return
  addingMember.value = true

  try {
    await $fetch(`${config.public.apiBase}/projects/${projectId}/assign_staff/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${useState('auth-access-token').value}`,
      },
      body: { user_id: selectedUserId.value },
    })

    await refreshMembers()
    showAddStaff.value = false
    selectedUserId.value = ''
  } catch (e: any) {
    error.value = e?.data?.error || 'Failed to add staff member'
  } finally {
    addingMember.value = false
  }
}

async function removeMember(userId: string) {
  try {
    await $fetch(`${config.public.apiBase}/projects/${projectId}/remove_member/`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${useState('auth-access-token').value}`,
      },
      body: { user_id: userId },
    })

    await refreshMembers()
  } catch (e: any) {
    error.value = e?.data?.error || 'Failed to remove member'
  }
}

// Delete project
const showDeleteConfirm = ref(false)
const deleting = ref(false)

async function handleDelete() {
  deleting.value = true
  error.value = ''

  try {
    await $fetch(`${config.public.apiBase}/projects/${projectId}/`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${useState('auth-access-token').value}`,
      },
    })

    await navigateTo('/admin/projects')
  } catch (e: any) {
    error.value = e?.data?.detail || 'Failed to delete project'
    deleting.value = false
    showDeleteConfirm.value = false
  }
}
</script>

<template>
  <div class="container py-8 max-w-4xl">
    <div class="flex items-center gap-4 mb-6">
      <Button variant="ghost" size="sm" as-child>
        <NuxtLink to="/admin/projects">
          <ArrowLeft class="h-4 w-4" />
        </NuxtLink>
      </Button>
      <div class="flex-1">
        <h1 class="text-3xl font-bold text-goal-dark">Edit Project</h1>
        <p class="text-muted-foreground">Update project details and manage team</p>
      </div>
    </div>

    <div v-if="pending" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-goal"></div>
    </div>

    <template v-else-if="projectData">
      <div class="grid gap-6 lg:grid-cols-3">
        <!-- Project Details -->
        <Card class="lg:col-span-2">
          <CardHeader>
            <CardTitle>Project Details</CardTitle>
            <CardDescription>Update the project information</CardDescription>
          </CardHeader>
          <CardContent>
            <form @submit.prevent="handleSubmit" class="space-y-6">
              <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-3 text-sm text-red-600">
                {{ error }}
              </div>
              <div v-if="success" class="bg-green-50 border border-green-200 rounded-md p-3 text-sm text-green-600">
                {{ success }}
              </div>

              <div class="space-y-2">
                <Label for="title">Project Title</Label>
                <Input id="title" v-model="form.title" required />
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                  <Label for="country">Country</Label>
                  <Input id="country" v-model="form.country" required />
                </div>
                <div class="space-y-2">
                  <Label for="country_area">Country Area / Region</Label>
                  <Input id="country_area" v-model="form.country_area" />
                </div>
              </div>

              <div class="space-y-2">
                <Label for="description">Description</Label>
                <textarea
                  id="description"
                  v-model="form.description"
                  rows="4"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                ></textarea>
              </div>

              <div class="flex justify-end gap-4 pt-4">
                <Button type="submit" :disabled="loading">
                  {{ loading ? 'Saving...' : 'Save Changes' }}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        <!-- Team Management -->
        <div class="space-y-6">
          <!-- Managers -->
          <Card>
            <CardHeader>
              <div class="flex items-center justify-between">
                <CardTitle class="text-lg">R4S Managers</CardTitle>
                <Button size="sm" variant="outline" @click="showAddManager = true">
                  <UserPlus class="h-4 w-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div v-if="!projectManagers.length" class="text-center py-4 text-muted-foreground text-sm">
                No managers assigned
              </div>
              <div v-else class="space-y-2">
                <div
                  v-for="member in projectManagers"
                  :key="member.id"
                  class="flex items-center justify-between p-2 rounded border"
                >
                  <div>
                    <div class="font-medium text-sm">{{ member.user?.full_name }}</div>
                    <div class="text-xs text-muted-foreground">{{ member.user?.email }}</div>
                  </div>
                  <Button size="sm" variant="ghost" @click="removeMember(member.user?.id)">
                    <X class="h-4 w-4 text-red-500" />
                  </Button>
                </div>
              </div>

              <!-- Add Manager Dialog -->
              <div v-if="showAddManager" class="mt-4 p-4 border rounded-lg bg-muted/50">
                <div class="space-y-3">
                  <Label>Select Manager</Label>
                  <select
                    v-model="selectedUserId"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  >
                    <option value="">Choose a manager...</option>
                    <option v-for="user in availableManagers" :key="user.id" :value="user.id">
                      {{ user.full_name }} ({{ user.email }})
                    </option>
                  </select>
                  <div v-if="!availableManagers.length" class="text-sm text-muted-foreground">
                    No available R4S Managers
                  </div>
                  <div class="flex gap-2">
                    <Button size="sm" variant="outline" @click="showAddManager = false">Cancel</Button>
                    <Button size="sm" @click="addManager" :disabled="!selectedUserId || addingMember">
                      {{ addingMember ? 'Adding...' : 'Add' }}
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- Staff -->
          <Card>
            <CardHeader>
              <div class="flex items-center justify-between">
                <CardTitle class="text-lg">Project Staff</CardTitle>
                <Button size="sm" variant="outline" @click="showAddStaff = true">
                  <UserPlus class="h-4 w-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div v-if="!projectStaff.length" class="text-center py-4 text-muted-foreground text-sm">
                No staff assigned
              </div>
              <div v-else class="space-y-2">
                <div
                  v-for="member in projectStaff"
                  :key="member.id"
                  class="flex items-center justify-between p-2 rounded border"
                >
                  <div>
                    <div class="font-medium text-sm">{{ member.user?.full_name }}</div>
                    <div class="text-xs text-muted-foreground">{{ member.user?.email }}</div>
                  </div>
                  <Button size="sm" variant="ghost" @click="removeMember(member.user?.id)">
                    <X class="h-4 w-4 text-red-500" />
                  </Button>
                </div>
              </div>

              <!-- Add Staff Dialog -->
              <div v-if="showAddStaff" class="mt-4 p-4 border rounded-lg bg-muted/50">
                <div class="space-y-3">
                  <Label>Select Staff Member</Label>
                  <select
                    v-model="selectedUserId"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  >
                    <option value="">Choose a staff member...</option>
                    <option v-for="user in availableStaff" :key="user.id" :value="user.id">
                      {{ user.full_name }} ({{ user.email }})
                    </option>
                  </select>
                  <div v-if="!availableStaff.length" class="text-sm text-muted-foreground">
                    No available Project Staff
                  </div>
                  <div class="flex gap-2">
                    <Button size="sm" variant="outline" @click="showAddStaff = false">Cancel</Button>
                    <Button size="sm" @click="addStaffMember" :disabled="!selectedUserId || addingMember">
                      {{ addingMember ? 'Adding...' : 'Add' }}
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- Danger Zone -->
      <Card class="border-red-200 mt-6">
        <CardHeader>
          <CardTitle class="text-red-600">Danger Zone</CardTitle>
          <CardDescription>Irreversible actions</CardDescription>
        </CardHeader>
        <CardContent>
          <div v-if="!showDeleteConfirm" class="flex items-center justify-between">
            <div>
              <p class="font-medium">Delete this project</p>
              <p class="text-sm text-muted-foreground">This will remove all team assignments</p>
            </div>
            <Button variant="destructive" @click="showDeleteConfirm = true">
              <Trash2 class="mr-2 h-4 w-4" />
              Delete Project
            </Button>
          </div>
          <div v-else class="space-y-4">
            <p class="text-red-600 font-medium">
              Are you sure you want to delete "{{ projectData.title }}"?
            </p>
            <div class="flex gap-4">
              <Button variant="outline" @click="showDeleteConfirm = false">
                Cancel
              </Button>
              <Button variant="destructive" @click="handleDelete" :disabled="deleting">
                {{ deleting ? 'Deleting...' : 'Yes, Delete Project' }}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </template>

    <div v-else class="text-center py-12 text-muted-foreground">
      Project not found
    </div>
  </div>
</template>
