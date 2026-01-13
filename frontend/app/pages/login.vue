<script setup lang="ts">
import { LogIn } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

definePageMeta({
  layout: 'auth',
})

useHead({
  title: 'Login - Resilio',
})

const { login, isAuthenticated } = useAuth()

// Redirect if already authenticated
if (isAuthenticated.value) {
  navigateTo('/')
}

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true

  const result = await login(email.value, password.value)

  loading.value = false

  if (result.success) {
    navigateTo('/')
  } else {
    error.value = result.error || 'Login failed'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-goal/5 to-transparent p-4">
    <Card class="w-full max-w-md">
      <CardHeader class="text-center">
        <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-goal text-white font-bold text-xl">
          R
        </div>
        <CardTitle class="text-2xl text-goal-dark">Welcome to Resilio</CardTitle>
        <CardDescription>Sign in to access R4S System Mapping</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div v-if="error" class="rounded-md bg-destructive/10 border border-destructive/20 p-3 text-sm text-destructive">
            {{ error }}
          </div>

          <div class="space-y-2">
            <label for="email" class="text-sm font-medium">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              autocomplete="email"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              placeholder="you@example.com"
            />
          </div>

          <div class="space-y-2">
            <label for="password" class="text-sm font-medium">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              placeholder="Enter your password"
            />
          </div>

          <Button type="submit" class="w-full" :disabled="loading">
            <LogIn v-if="!loading" class="mr-2 h-4 w-4" />
            <span v-if="loading" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
            {{ loading ? 'Signing in...' : 'Sign in' }}
          </Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
