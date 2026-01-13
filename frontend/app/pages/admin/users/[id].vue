<script setup lang="ts">
import { ArrowLeft, Trash2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'

const route = useRoute()
const userId = route.params.id

useHead({
  title: 'Edit User - Admin - Resilio',
})

const { isAuthenticated, isSuperadmin, user: currentUser } = useAuth()
const config = useRuntimeConfig()

onMounted(() => {
  if (!isAuthenticated.value || !isSuperadmin.value) {
    navigateTo('/')
  }
})

const { data: userData, pending } = await useFetch<any>(
  `${config.public.apiBase}/users/${userId}/`,
  {
    headers: {
      Authorization: `Bearer ${useState('auth-access-token').value}`,
    },
  }
)

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  role: 'project_staff',
  is_active: true,
  title: '',
  country: '',
  department: '',
  job_title: '',
})

watch(userData, (user) => {
  if (user) {
    form.first_name = user.first_name || ''
    form.last_name = user.last_name || ''
    form.email = user.email || ''
    form.role = user.role || 'project_staff'
    form.is_active = user.is_active ?? true
    form.title = user.title || ''
    form.country = user.country || ''
    form.department = user.department || ''
    form.job_title = user.job_title || ''
  }
}, { immediate: true })

const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    await $fetch(`${config.public.apiBase}/users/${userId}/`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${useState('auth-access-token').value}`,
      },
      body: form,
    })

    success.value = 'User updated successfully'
  } catch (e: any) {
    error.value = e?.data?.detail || 'Failed to update user'
  } finally {
    loading.value = false
  }
}

const showDeleteConfirm = ref(false)
const deleting = ref(false)

async function handleDelete() {
  if (userData.value?.id === currentUser.value?.id) {
    error.value = 'You cannot delete your own account'
    return
  }

  deleting.value = true
  error.value = ''

  try {
    await $fetch(`${config.public.apiBase}/users/${userId}/`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${useState('auth-access-token').value}`,
      },
    })

    await navigateTo('/admin/users')
  } catch (e: any) {
    error.value = e?.data?.detail || 'Failed to delete user'
    deleting.value = false
    showDeleteConfirm.value = false
  }
}
</script>

<template>
  <div class="container py-8 max-w-2xl">
    <div class="flex items-center gap-4 mb-6">
      <Button variant="ghost" size="sm" as-child>
        <NuxtLink to="/admin/users">
          <ArrowLeft class="h-4 w-4" />
        </NuxtLink>
      </Button>
      <div class="flex-1">
        <h1 class="text-3xl font-bold text-goal-dark">Edit User</h1>
        <p class="text-muted-foreground">Update user details and permissions</p>
      </div>
    </div>

    <div v-if="pending" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-goal"></div>
    </div>

    <template v-else-if="userData">
      <Card class="mb-6">
        <CardHeader>
          <div class="flex items-center justify-between">
            <div>
              <CardTitle>{{ userData.full_name || userData.email }}</CardTitle>
              <CardDescription>{{ userData.email }}</CardDescription>
            </div>
            <Badge :variant="userData.is_active ? 'default' : 'destructive'">
              {{ userData.is_active ? 'Active' : 'Inactive' }}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-3 text-sm text-red-600">
              {{ error }}
            </div>
            <div v-if="success" class="bg-green-50 border border-green-200 rounded-md p-3 text-sm text-green-600">
              {{ success }}
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="first_name">First Name</Label>
                <Input id="first_name" v-model="form.first_name" required />
              </div>
              <div class="space-y-2">
                <Label for="last_name">Last Name</Label>
                <Input id="last_name" v-model="form.last_name" required />
              </div>
            </div>

            <div class="space-y-2">
              <Label for="email">Email</Label>
              <Input id="email" v-model="form.email" type="email" required />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="role">Role</Label>
                <select
                  id="role"
                  v-model="form.role"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="superadmin">Superadmin</option>
                  <option value="r4s_manager">R4S Manager</option>
                  <option value="project_staff">Project Staff</option>
                </select>
              </div>
              <div class="space-y-2">
                <Label for="is_active">Status</Label>
                <select
                  id="is_active"
                  v-model="form.is_active"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option :value="true">Active</option>
                  <option :value="false">Inactive</option>
                </select>
              </div>
            </div>

            <div class="border-t pt-6 mt-6">
              <h3 class="font-medium mb-4">Profile Information</h3>
              <div class="space-y-4">
                <div class="space-y-2">
                  <Label for="title">Title</Label>
                  <Input id="title" v-model="form.title" placeholder="e.g., Dr., Mr., Ms." />
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div class="space-y-2">
                    <Label for="country">Country</Label>
                    <Input id="country" v-model="form.country" />
                  </div>
                  <div class="space-y-2">
                    <Label for="department">Department</Label>
                    <Input id="department" v-model="form.department" />
                  </div>
                </div>

                <div class="space-y-2">
                  <Label for="job_title">Job Title</Label>
                  <Input id="job_title" v-model="form.job_title" />
                </div>
              </div>
            </div>

            <div class="flex justify-end gap-4 pt-4">
              <Button variant="outline" type="button" as-child>
                <NuxtLink to="/admin/users">Cancel</NuxtLink>
              </Button>
              <Button type="submit" :disabled="loading">
                {{ loading ? 'Saving...' : 'Save Changes' }}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <!-- Danger Zone -->
      <Card class="border-red-200">
        <CardHeader>
          <CardTitle class="text-red-600">Danger Zone</CardTitle>
          <CardDescription>Irreversible actions</CardDescription>
        </CardHeader>
        <CardContent>
          <div v-if="!showDeleteConfirm" class="flex items-center justify-between">
            <div>
              <p class="font-medium">Delete this user</p>
              <p class="text-sm text-muted-foreground">This action cannot be undone</p>
            </div>
            <Button
              variant="destructive"
              @click="showDeleteConfirm = true"
              :disabled="userData.id === currentUser?.id"
            >
              <Trash2 class="mr-2 h-4 w-4" />
              Delete User
            </Button>
          </div>
          <div v-else class="space-y-4">
            <p class="text-red-600 font-medium">
              Are you sure you want to delete {{ userData.full_name || userData.email }}?
            </p>
            <div class="flex gap-4">
              <Button variant="outline" @click="showDeleteConfirm = false">
                Cancel
              </Button>
              <Button variant="destructive" @click="handleDelete" :disabled="deleting">
                {{ deleting ? 'Deleting...' : 'Yes, Delete User' }}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </template>

    <div v-else class="text-center py-12 text-muted-foreground">
      User not found
    </div>
  </div>
</template>
