<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

useHead({
  title: 'Create Project - Admin - Resilio',
})

const { isAuthenticated, isSuperadmin } = useAuth()
const config = useRuntimeConfig()

onMounted(() => {
  if (!isAuthenticated.value || !isSuperadmin.value) {
    navigateTo('/')
  }
})

const form = reactive({
  title: '',
  country: '',
  country_area: '',
  description: '',
})

const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''

  try {
    const project = await $fetch<any>(`${config.public.apiBase}/projects/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${useState('auth-access-token').value}`,
      },
      body: form,
    })

    await navigateTo(`/admin/projects/${project.id}`)
  } catch (e: any) {
    error.value = e?.data?.detail || e?.data?.title?.[0] || 'Failed to create project'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container py-8 max-w-2xl">
    <div class="flex items-center gap-4 mb-6">
      <Button variant="ghost" size="sm" as-child>
        <NuxtLink to="/admin/projects">
          <ArrowLeft class="h-4 w-4" />
        </NuxtLink>
      </Button>
      <div>
        <h1 class="text-3xl font-bold text-goal-dark">Create Project</h1>
        <p class="text-muted-foreground">Add a new R4S project</p>
      </div>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>Project Details</CardTitle>
        <CardDescription>Enter the information for the new project</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-3 text-sm text-red-600">
            {{ error }}
          </div>

          <div class="space-y-2">
            <Label for="title">Project Title</Label>
            <Input id="title" v-model="form.title" required placeholder="e.g., RMNCAH Health System Mapping" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="country">Country</Label>
              <Input id="country" v-model="form.country" required placeholder="e.g., Ethiopia" />
            </div>
            <div class="space-y-2">
              <Label for="country_area">Country Area / Region</Label>
              <Input id="country_area" v-model="form.country_area" placeholder="e.g., Eastern Region" />
            </div>
          </div>

          <div class="space-y-2">
            <Label for="description">Description</Label>
            <textarea
              id="description"
              v-model="form.description"
              rows="4"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Brief description of the project..."
            ></textarea>
          </div>

          <div class="flex justify-end gap-4 pt-4">
            <Button variant="outline" type="button" as-child>
              <NuxtLink to="/admin/projects">Cancel</NuxtLink>
            </Button>
            <Button type="submit" :disabled="loading">
              {{ loading ? 'Creating...' : 'Create Project' }}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
