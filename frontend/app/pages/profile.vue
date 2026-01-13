<script setup lang="ts">
import { Save, Key, User as UserIcon } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

useHead({
  title: 'Profile - Resilio',
})

const { user, updateProfile, changePassword, isAuthenticated } = useAuth()

// Redirect if not authenticated
if (!isAuthenticated.value) {
  navigateTo('/login')
}

// Profile form
const profileForm = ref({
  first_name: user.value?.first_name || '',
  last_name: user.value?.last_name || '',
  title: user.value?.title || '',
  country: user.value?.country || '',
  department: user.value?.department || '',
  job_title: user.value?.job_title || '',
})
const profileError = ref('')
const profileSuccess = ref('')
const profileLoading = ref(false)

// Password form
const passwordForm = ref({
  old_password: '',
  new_password: '',
  new_password_confirm: '',
})
const passwordError = ref('')
const passwordSuccess = ref('')
const passwordLoading = ref(false)

// Watch for user changes
watch(user, (newUser) => {
  if (newUser) {
    profileForm.value = {
      first_name: newUser.first_name,
      last_name: newUser.last_name,
      title: newUser.title,
      country: newUser.country,
      department: newUser.department,
      job_title: newUser.job_title,
    }
  }
}, { immediate: true })

async function handleProfileSubmit() {
  profileError.value = ''
  profileSuccess.value = ''
  profileLoading.value = true

  const result = await updateProfile(profileForm.value)

  profileLoading.value = false

  if (result.success) {
    profileSuccess.value = 'Profile updated successfully'
  } else {
    profileError.value = result.error || 'Failed to update profile'
  }
}

async function handlePasswordSubmit() {
  passwordError.value = ''
  passwordSuccess.value = ''
  passwordLoading.value = true

  const result = await changePassword(
    passwordForm.value.old_password,
    passwordForm.value.new_password,
    passwordForm.value.new_password_confirm
  )

  passwordLoading.value = false

  if (result.success) {
    passwordSuccess.value = 'Password changed successfully'
    passwordForm.value = {
      old_password: '',
      new_password: '',
      new_password_confirm: '',
    }
  } else {
    passwordError.value = result.error || 'Failed to change password'
  }
}

const roleVariant = computed(() => {
  switch (user.value?.role) {
    case 'superadmin': return 'default'
    case 'r4s_manager': return 'secondary'
    default: return 'outline'
  }
})
</script>

<template>
  <div class="container py-8 max-w-3xl">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-goal-dark">Profile</h1>
      <p class="text-muted-foreground mt-1">Manage your account settings</p>
    </div>

    <!-- User Info Card -->
    <Card class="mb-6">
      <CardHeader>
        <div class="flex items-center gap-4">
          <div class="flex h-16 w-16 items-center justify-center rounded-full bg-goal/10 text-goal">
            <UserIcon class="h-8 w-8" />
          </div>
          <div>
            <CardTitle>{{ user?.full_name }}</CardTitle>
            <CardDescription>{{ user?.email }}</CardDescription>
            <Badge :variant="roleVariant" class="mt-2">{{ user?.role_display }}</Badge>
          </div>
        </div>
      </CardHeader>
    </Card>

    <!-- Profile Form -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle>Personal Information</CardTitle>
        <CardDescription>Update your profile details</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleProfileSubmit" class="space-y-4">
          <div v-if="profileError" class="rounded-md bg-destructive/10 border border-destructive/20 p-3 text-sm text-destructive">
            {{ profileError }}
          </div>
          <div v-if="profileSuccess" class="rounded-md bg-green-50 border border-green-200 p-3 text-sm text-green-700">
            {{ profileSuccess }}
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <label for="first_name" class="text-sm font-medium">First Name</label>
              <input
                id="first_name"
                v-model="profileForm.first_name"
                type="text"
                required
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
            <div class="space-y-2">
              <label for="last_name" class="text-sm font-medium">Last Name</label>
              <input
                id="last_name"
                v-model="profileForm.last_name"
                type="text"
                required
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
          </div>

          <div class="space-y-2">
            <label for="title" class="text-sm font-medium">Title</label>
            <input
              id="title"
              v-model="profileForm.title"
              type="text"
              placeholder="e.g., Mr, Ms, Dr"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            />
          </div>

          <div class="space-y-2">
            <label for="country" class="text-sm font-medium">Country</label>
            <input
              id="country"
              v-model="profileForm.country"
              type="text"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <label for="department" class="text-sm font-medium">Department</label>
              <input
                id="department"
                v-model="profileForm.department"
                type="text"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
            <div class="space-y-2">
              <label for="job_title" class="text-sm font-medium">Job Title</label>
              <input
                id="job_title"
                v-model="profileForm.job_title"
                type="text"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
          </div>

          <Button type="submit" :disabled="profileLoading">
            <Save v-if="!profileLoading" class="mr-2 h-4 w-4" />
            <span v-if="profileLoading" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
            {{ profileLoading ? 'Saving...' : 'Save Changes' }}
          </Button>
        </form>
      </CardContent>
    </Card>

    <!-- Password Form -->
    <Card>
      <CardHeader>
        <CardTitle>Change Password</CardTitle>
        <CardDescription>Update your password</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handlePasswordSubmit" class="space-y-4">
          <div v-if="passwordError" class="rounded-md bg-destructive/10 border border-destructive/20 p-3 text-sm text-destructive">
            {{ passwordError }}
          </div>
          <div v-if="passwordSuccess" class="rounded-md bg-green-50 border border-green-200 p-3 text-sm text-green-700">
            {{ passwordSuccess }}
          </div>

          <div class="space-y-2">
            <label for="old_password" class="text-sm font-medium">Current Password</label>
            <input
              id="old_password"
              v-model="passwordForm.old_password"
              type="password"
              required
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            />
          </div>

          <div class="space-y-2">
            <label for="new_password" class="text-sm font-medium">New Password</label>
            <input
              id="new_password"
              v-model="passwordForm.new_password"
              type="password"
              required
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            />
          </div>

          <div class="space-y-2">
            <label for="new_password_confirm" class="text-sm font-medium">Confirm New Password</label>
            <input
              id="new_password_confirm"
              v-model="passwordForm.new_password_confirm"
              type="password"
              required
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            />
          </div>

          <Button type="submit" variant="outline" :disabled="passwordLoading">
            <Key v-if="!passwordLoading" class="mr-2 h-4 w-4" />
            <span v-if="passwordLoading" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
            {{ passwordLoading ? 'Changing...' : 'Change Password' }}
          </Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
