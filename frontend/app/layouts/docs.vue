<script setup lang="ts">
import {
  Book, Server, Database, Code, Rocket, Users, Network,
  Shield, Cpu, FileText, ChevronRight, Menu, X, Home,
  ExternalLink, Github, ClipboardCheck, Wrench
} from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

const { isAuthenticated } = useAuth()
const route = useRoute()

// Redirect if not authenticated
if (import.meta.client && !isAuthenticated.value) {
  navigateTo('/login')
}

const sidebarOpen = ref(false)

const navigation = [
  {
    title: 'Getting Started',
    items: [
      { name: 'Overview', href: '/docs', icon: Book },
      { name: 'Architecture', href: '/docs/architecture', icon: Server },
      { name: 'Quick Start', href: '/docs/quickstart', icon: Rocket },
    ]
  },
  {
    title: 'Core Concepts',
    items: [
      { name: 'Systems & Actors', href: '/docs/systems', icon: Network },
      { name: 'Data Models', href: '/docs/models', icon: Database },
      { name: 'Authentication', href: '/docs/authentication', icon: Shield },
    ]
  },
  {
    title: 'API Reference',
    items: [
      { name: 'REST API', href: '/docs/api', icon: Code },
      { name: 'Endpoints', href: '/docs/endpoints', icon: FileText },
      { name: 'DSL Specification', href: '/docs/dsl', icon: FileText },
    ]
  },
  {
    title: 'Deployment',
    items: [
      { name: 'AWS Infrastructure', href: '/docs/aws', icon: Cpu },
      { name: 'Configuration', href: '/docs/configuration', icon: FileText },
      { name: 'Well-Architected Review', href: '/docs/well-architected', icon: ClipboardCheck },
      { name: 'Operations Runbook', href: '/docs/runbook', icon: Wrench },
    ]
  }
]

function isActive(href: string) {
  return route.path === href
}
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Mobile sidebar toggle -->
    <div class="lg:hidden fixed top-16 left-4 z-50">
      <Button variant="outline" size="icon" @click="sidebarOpen = !sidebarOpen">
        <Menu v-if="!sidebarOpen" class="h-5 w-5" />
        <X v-else class="h-5 w-5" />
      </Button>
    </div>

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed top-16 left-0 z-40 h-[calc(100vh-4rem)] w-72 border-r-2 border-gray-300 bg-white shadow-sm transition-transform duration-200 ease-in-out overflow-y-auto',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      ]"
    >
      <div class="p-6">
        <!-- Logo/Title -->
        <div class="flex items-center gap-3 mb-8">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
            <Book class="h-5 w-5 text-goal" />
          </div>
          <div>
            <h2 class="font-semibold text-goal-dark">Documentation</h2>
            <p class="text-xs text-muted-foreground">v2.1.0</p>
          </div>
        </div>

        <!-- Navigation -->
        <nav class="space-y-6">
          <div v-for="section in navigation" :key="section.title">
            <h3 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
              {{ section.title }}
            </h3>
            <ul class="space-y-1">
              <li v-for="item in section.items" :key="item.name">
                <NuxtLink
                  :to="item.href"
                  :class="[
                    'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors',
                    isActive(item.href)
                      ? 'bg-goal/10 text-goal font-medium'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  ]"
                  @click="sidebarOpen = false"
                >
                  <component :is="item.icon" class="h-4 w-4" />
                  {{ item.name }}
                </NuxtLink>
              </li>
            </ul>
          </div>
        </nav>

        <!-- Footer Links -->
        <div class="mt-8 pt-6 border-t">
          <div class="space-y-2">
            <NuxtLink
              to="/systems"
              class="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
            >
              <Home class="h-4 w-4" />
              Back to App
            </NuxtLink>
            <a
              href="https://github.com/data-friendly-space/AWS-Hackaton-Dublin"
              target="_blank"
              class="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
            >
              <Github class="h-4 w-4" />
              GitHub Repository
              <ExternalLink class="h-3 w-3" />
            </a>
          </div>
        </div>
      </div>
    </aside>

    <!-- Overlay for mobile -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-30 bg-black/50 lg:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Main content -->
    <main class="lg:pl-72">
      <div class="max-w-4xl mx-auto px-6 py-12 bg-white min-h-screen shadow-sm">
        <slot />
      </div>
    </main>
  </div>
</template>
