<script setup lang="ts">
definePageMeta({
  layout: 'auth',
})

useHead({
  title: 'Login - Resilio',
})

const { login, isAuthenticated } = useAuth()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

// Use onMounted for client-side redirect check to avoid hydration issues
onMounted(() => {
  if (isAuthenticated.value) {
    navigateTo('/')
  }
})

async function handleSubmit() {
  error.value = ''
  loading.value = true

  try {
    const result = await login(email.value, password.value)

    if (result.success) {
      await navigateTo('/')
    } else {
      error.value = result.error || 'Login failed'
    }
  } catch (e) {
    error.value = 'An unexpected error occurred'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 p-4">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
      <div class="text-center mb-6">
        <img src="/logo.svg" alt="Resilio" class="mx-auto mb-4 h-16 w-16" />
        <h1 class="text-2xl font-bold text-gray-900">Welcome to Resilio</h1>
        <p class="text-gray-600">Sign in to access R4S System Mapping</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-3 text-sm text-red-600">
          {{ error }}
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Enter your password"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2 px-4 bg-green-600 hover:bg-green-700 text-white font-medium rounded-md disabled:opacity-50 transition-colors"
        >
          {{ loading ? 'Signing in...' : 'Sign in' }}
        </button>
      </form>
    </div>
  </div>
</template>
