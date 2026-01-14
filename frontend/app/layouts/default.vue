<script setup lang="ts">
import { User, LogOut, Settings, Shield } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

const { user, isAuthenticated, isSuperadmin, logout } = useAuth()
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <!-- Header -->
    <header class="sticky top-0 z-50 w-full border-b-2 border-gray-300 bg-white shadow-sm">
      <div class="container flex h-16 items-center justify-between">
        <div class="flex items-center gap-4">
          <NuxtLink to="/" class="flex items-center gap-2">
            <img src="/logo.svg" alt="Resilio" class="h-8 w-8" />
            <span class="text-xl font-bold text-goal-dark">Resilio</span>
          </NuxtLink>
          <span class="text-sm text-gray-500 hidden sm:inline">
            R4S System Mapping
          </span>
        </div>

        <nav class="flex items-center gap-4">
          <NuxtLink
            v-if="isAuthenticated"
            to="/systems"
            class="text-sm font-medium text-gray-600 transition-colors hover:text-gray-900"
          >
            Systems
          </NuxtLink>

          <NuxtLink
            v-if="isAuthenticated"
            to="/docs"
            class="text-sm font-medium text-gray-600 transition-colors hover:text-gray-900"
          >
            Docs
          </NuxtLink>

          <template v-if="isAuthenticated && isSuperadmin">
            <NuxtLink
              to="/admin"
              class="text-sm font-medium text-gray-600 transition-colors hover:text-gray-900"
            >
              Admin
            </NuxtLink>
          </template>

          <NuxtLink
            to="/about"
            class="text-sm font-medium text-gray-600 transition-colors hover:text-gray-900"
          >
            About
          </NuxtLink>

          <!-- Auth Section -->
          <div class="flex items-center gap-2 ml-4 pl-4 border-l-2 border-gray-300">
            <template v-if="isAuthenticated">
              <NuxtLink
                to="/profile"
                class="flex items-center gap-2 text-sm font-medium text-gray-600 transition-colors hover:text-gray-900"
              >
                <User class="h-4 w-4" />
                <span class="hidden sm:inline">{{ user?.first_name }}</span>
              </NuxtLink>
              <Button variant="ghost" size="sm" @click="logout">
                <LogOut class="h-4 w-4" />
              </Button>
            </template>
            <template v-else>
              <Button variant="default" size="sm" as-child>
                <NuxtLink to="/login">Sign in</NuxtLink>
              </Button>
            </template>
          </div>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="border-t bg-goal-dark text-white">
      <div class="container py-8">
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="flex items-center gap-2">
            <span class="text-sm">Powered by</span>
            <span class="font-semibold">GOAL Global</span>
            <span class="text-sm text-white/70">R4S Methodology</span>
          </div>
          <div class="text-sm text-white/70">
            Built for AWS Generative AI Hackathon 2025
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>
