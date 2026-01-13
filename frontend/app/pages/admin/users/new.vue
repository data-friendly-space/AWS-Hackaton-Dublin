<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

useHead({
  title: 'Create User - Admin - Resilio',
})

const { isAuthenticated, isSuperadmin } = useAuth()
const config = useRuntimeConfig()

onMounted(() => {
  if (!isAuthenticated.value || !isSuperadmin.value) {
    navigateTo('/')
  }
})

const form = reactive({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  role: 'project_staff',
  title: '',
  country: '',
  department: '',
  job_title: '',
})

const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''

  try {
    await $fetch(`${config.public.apiBase}/users/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${useState('auth-access-token').value}`,
      },
      body: form,
    })

    await navigateTo('/admin/users')
  } catch (e: any) {
    error.value = e?.data?.detail || e?.data?.email?.[0] || e?.data?.password?.[0] || 'Failed to create user'
  } finally {
    loading.value = false
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
      <div>
        <h1 class="text-3xl font-bold text-goal-dark">Create User</h1>
        <p class="text-muted-foreground">Add a new user to the system</p>
      </div>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>User Details</CardTitle>
        <CardDescription>Enter the information for the new user</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-3 text-sm text-red-600">
            {{ error }}
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

          <div class="space-y-2">
            <Label for="password">Password</Label>
            <Input id="password" v-model="form.password" type="password" required />
          </div>

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
              {{ loading ? 'Creating...' : 'Create User' }}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
