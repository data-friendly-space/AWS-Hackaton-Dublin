<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'API Endpoints - Documentation - Resilio',
})

const endpoints = {
  systems: [
    { method: 'GET', path: '/api/systems/', description: 'List all systems with pagination', auth: true },
    { method: 'POST', path: '/api/systems/', description: 'Create a new system', auth: true, role: 'r4s_manager+' },
    { method: 'GET', path: '/api/systems/{slug}/', description: 'Get system details by slug', auth: true },
    { method: 'PUT', path: '/api/systems/{slug}/', description: 'Update entire system', auth: true, role: 'owner' },
    { method: 'PATCH', path: '/api/systems/{slug}/', description: 'Partial update system', auth: true, role: 'owner' },
    { method: 'DELETE', path: '/api/systems/{slug}/', description: 'Delete a system', auth: true, role: 'superadmin' },
    { method: 'GET', path: '/api/systems/{slug}/export/', description: 'Export system as JSON', auth: true },
    { method: 'POST', path: '/api/systems/{slug}/duplicate/', description: 'Duplicate a system', auth: true, role: 'r4s_manager+' },
  ],
  actors: [
    { method: 'GET', path: '/api/actors/', description: 'List all actors', auth: true },
    { method: 'POST', path: '/api/actors/', description: 'Create a new actor', auth: true },
    { method: 'GET', path: '/api/actors/{id}/', description: 'Get actor details', auth: true },
    { method: 'PUT', path: '/api/actors/{id}/', description: 'Update actor', auth: true },
    { method: 'PATCH', path: '/api/actors/{id}/', description: 'Partial update actor', auth: true },
    { method: 'DELETE', path: '/api/actors/{id}/', description: 'Delete actor', auth: true },
    { method: 'GET', path: '/api/actors/by-system/{system_id}/', description: 'List actors for a system', auth: true },
  ],
  relationships: [
    { method: 'GET', path: '/api/relationships/', description: 'List all relationships', auth: true },
    { method: 'POST', path: '/api/relationships/', description: 'Create a relationship', auth: true },
    { method: 'GET', path: '/api/relationships/{id}/', description: 'Get relationship details', auth: true },
    { method: 'PUT', path: '/api/relationships/{id}/', description: 'Update relationship', auth: true },
    { method: 'PATCH', path: '/api/relationships/{id}/', description: 'Partial update relationship', auth: true },
    { method: 'DELETE', path: '/api/relationships/{id}/', description: 'Delete relationship', auth: true },
    { method: 'GET', path: '/api/relationships/by-system/{system_id}/', description: 'List relationships for a system', auth: true },
  ],
  risks: [
    { method: 'GET', path: '/api/risks/', description: 'List all risk scenarios', auth: true },
    { method: 'POST', path: '/api/risks/', description: 'Create a risk scenario', auth: true },
    { method: 'GET', path: '/api/risks/{id}/', description: 'Get risk details', auth: true },
    { method: 'PUT', path: '/api/risks/{id}/', description: 'Update risk scenario', auth: true },
    { method: 'PATCH', path: '/api/risks/{id}/', description: 'Partial update risk', auth: true },
    { method: 'DELETE', path: '/api/risks/{id}/', description: 'Delete risk scenario', auth: true },
    { method: 'GET', path: '/api/risks/by-system/{system_id}/', description: 'List risks for a system', auth: true },
  ],
  components: [
    { method: 'GET', path: '/api/components/', description: 'List all components', auth: true },
    { method: 'POST', path: '/api/components/', description: 'Create a component', auth: true },
    { method: 'GET', path: '/api/components/{id}/', description: 'Get component details', auth: true },
    { method: 'PUT', path: '/api/components/{id}/', description: 'Update component', auth: true },
    { method: 'PATCH', path: '/api/components/{id}/', description: 'Partial update component', auth: true },
    { method: 'DELETE', path: '/api/components/{id}/', description: 'Delete component', auth: true },
  ],
  projects: [
    { method: 'GET', path: '/api/projects/', description: 'List all projects', auth: true },
    { method: 'POST', path: '/api/projects/', description: 'Create a new project', auth: true, role: 'r4s_manager+' },
    { method: 'GET', path: '/api/projects/{slug}/', description: 'Get project details', auth: true },
    { method: 'PUT', path: '/api/projects/{slug}/', description: 'Update project', auth: true, role: 'owner' },
    { method: 'DELETE', path: '/api/projects/{slug}/', description: 'Delete project', auth: true, role: 'superadmin' },
    { method: 'POST', path: '/api/projects/{slug}/add-member/', description: 'Add member to project', auth: true, role: 'r4s_manager+' },
    { method: 'POST', path: '/api/projects/{slug}/remove-member/', description: 'Remove member from project', auth: true, role: 'r4s_manager+' },
  ],
  users: [
    { method: 'GET', path: '/api/users/', description: 'List all users', auth: true, role: 'superadmin' },
    { method: 'POST', path: '/api/users/', description: 'Create a new user', auth: true, role: 'superadmin' },
    { method: 'GET', path: '/api/users/me/', description: 'Get current user profile', auth: true },
    { method: 'PATCH', path: '/api/users/me/', description: 'Update current user profile', auth: true },
    { method: 'GET', path: '/api/users/{id}/', description: 'Get user by ID', auth: true, role: 'superadmin' },
    { method: 'PUT', path: '/api/users/{id}/', description: 'Update user', auth: true, role: 'superadmin' },
    { method: 'DELETE', path: '/api/users/{id}/', description: 'Delete user', auth: true, role: 'superadmin' },
    { method: 'POST', path: '/api/users/change_password/', description: 'Change password', auth: true },
  ],
  auth: [
    { method: 'POST', path: '/api/auth/login/', description: 'Login and get JWT tokens', auth: false },
    { method: 'POST', path: '/api/auth/refresh/', description: 'Refresh access token', auth: false },
    { method: 'POST', path: '/api/auth/logout/', description: 'Logout (blacklist token)', auth: true },
    { method: 'POST', path: '/api/auth/register/', description: 'Register new user', auth: false },
    { method: 'POST', path: '/api/auth/forgot-password/', description: 'Request password reset', auth: false },
    { method: 'POST', path: '/api/auth/reset-password/', description: 'Reset password with token', auth: false },
  ],
  ai: [
    { method: 'POST', path: '/api/ai/analyze/', description: 'Get AI analysis of a system', auth: true },
    { method: 'POST', path: '/api/ai/chat/', description: 'Chat with AI about system data', auth: true },
    { method: 'POST', path: '/api/ai/recommendations/', description: 'Get AI recommendations', auth: true },
    { method: 'GET', path: '/api/ai/models/', description: 'List available AI models', auth: true },
  ]
}

function getMethodColor(method: string) {
  const colors: Record<string, string> = {
    GET: 'bg-blue-600',
    POST: 'bg-green-600',
    PUT: 'bg-amber-600',
    PATCH: 'bg-amber-600',
    DELETE: 'bg-red-600'
  }
  return colors[method] || 'bg-gray-600'
}
</script>

<template>
  <div>
    <Badge class="mb-4">API Reference</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">API Endpoints</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Complete list of all available API endpoints organized by resource.
    </p>

    <!-- Quick Navigation -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle>Quick Navigation</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="flex flex-wrap gap-2">
          <a href="#systems" class="text-sm text-goal hover:underline">Systems</a>
          <span class="text-muted-foreground">|</span>
          <a href="#actors" class="text-sm text-goal hover:underline">Actors</a>
          <span class="text-muted-foreground">|</span>
          <a href="#relationships" class="text-sm text-goal hover:underline">Relationships</a>
          <span class="text-muted-foreground">|</span>
          <a href="#risks" class="text-sm text-goal hover:underline">Risks</a>
          <span class="text-muted-foreground">|</span>
          <a href="#components" class="text-sm text-goal hover:underline">Components</a>
          <span class="text-muted-foreground">|</span>
          <a href="#projects" class="text-sm text-goal hover:underline">Projects</a>
          <span class="text-muted-foreground">|</span>
          <a href="#users" class="text-sm text-goal hover:underline">Users</a>
          <span class="text-muted-foreground">|</span>
          <a href="#auth" class="text-sm text-goal hover:underline">Authentication</a>
          <span class="text-muted-foreground">|</span>
          <a href="#ai" class="text-sm text-goal hover:underline">AI</a>
        </div>
      </CardContent>
    </Card>

    <!-- Systems -->
    <div id="systems" class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Systems</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Method</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Endpoint</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Description</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Auth</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(endpoint, idx) in endpoints.systems" :key="idx" class="border-b last:border-0">
                  <td class="py-2 px-3">
                    <Badge :class="getMethodColor(endpoint.method)" class="text-xs">{{ endpoint.method }}</Badge>
                  </td>
                  <td class="py-2 px-3 font-mono text-sm">{{ endpoint.path }}</td>
                  <td class="py-2 px-3 text-sm text-muted-foreground">{{ endpoint.description }}</td>
                  <td class="py-2 px-3">
                    <Badge v-if="endpoint.role" variant="outline" class="text-xs">{{ endpoint.role }}</Badge>
                    <Badge v-else-if="endpoint.auth" variant="outline" class="text-xs">Required</Badge>
                    <span v-else class="text-xs text-muted-foreground">Public</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Actors -->
    <div id="actors" class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Actors</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Method</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Endpoint</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Description</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Auth</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(endpoint, idx) in endpoints.actors" :key="idx" class="border-b last:border-0">
                  <td class="py-2 px-3">
                    <Badge :class="getMethodColor(endpoint.method)" class="text-xs">{{ endpoint.method }}</Badge>
                  </td>
                  <td class="py-2 px-3 font-mono text-sm">{{ endpoint.path }}</td>
                  <td class="py-2 px-3 text-sm text-muted-foreground">{{ endpoint.description }}</td>
                  <td class="py-2 px-3">
                    <Badge v-if="endpoint.auth" variant="outline" class="text-xs">Required</Badge>
                    <span v-else class="text-xs text-muted-foreground">Public</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Relationships -->
    <div id="relationships" class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Relationships</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Method</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Endpoint</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Description</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Auth</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(endpoint, idx) in endpoints.relationships" :key="idx" class="border-b last:border-0">
                  <td class="py-2 px-3">
                    <Badge :class="getMethodColor(endpoint.method)" class="text-xs">{{ endpoint.method }}</Badge>
                  </td>
                  <td class="py-2 px-3 font-mono text-sm">{{ endpoint.path }}</td>
                  <td class="py-2 px-3 text-sm text-muted-foreground">{{ endpoint.description }}</td>
                  <td class="py-2 px-3">
                    <Badge v-if="endpoint.auth" variant="outline" class="text-xs">Required</Badge>
                    <span v-else class="text-xs text-muted-foreground">Public</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Risks -->
    <div id="risks" class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Risk Scenarios</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Method</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Endpoint</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Description</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Auth</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(endpoint, idx) in endpoints.risks" :key="idx" class="border-b last:border-0">
                  <td class="py-2 px-3">
                    <Badge :class="getMethodColor(endpoint.method)" class="text-xs">{{ endpoint.method }}</Badge>
                  </td>
                  <td class="py-2 px-3 font-mono text-sm">{{ endpoint.path }}</td>
                  <td class="py-2 px-3 text-sm text-muted-foreground">{{ endpoint.description }}</td>
                  <td class="py-2 px-3">
                    <Badge v-if="endpoint.auth" variant="outline" class="text-xs">Required</Badge>
                    <span v-else class="text-xs text-muted-foreground">Public</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Components -->
    <div id="components" class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Components</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Method</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Endpoint</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Description</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Auth</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(endpoint, idx) in endpoints.components" :key="idx" class="border-b last:border-0">
                  <td class="py-2 px-3">
                    <Badge :class="getMethodColor(endpoint.method)" class="text-xs">{{ endpoint.method }}</Badge>
                  </td>
                  <td class="py-2 px-3 font-mono text-sm">{{ endpoint.path }}</td>
                  <td class="py-2 px-3 text-sm text-muted-foreground">{{ endpoint.description }}</td>
                  <td class="py-2 px-3">
                    <Badge v-if="endpoint.auth" variant="outline" class="text-xs">Required</Badge>
                    <span v-else class="text-xs text-muted-foreground">Public</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Projects -->
    <div id="projects" class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Projects</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Method</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Endpoint</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Description</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Auth</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(endpoint, idx) in endpoints.projects" :key="idx" class="border-b last:border-0">
                  <td class="py-2 px-3">
                    <Badge :class="getMethodColor(endpoint.method)" class="text-xs">{{ endpoint.method }}</Badge>
                  </td>
                  <td class="py-2 px-3 font-mono text-sm">{{ endpoint.path }}</td>
                  <td class="py-2 px-3 text-sm text-muted-foreground">{{ endpoint.description }}</td>
                  <td class="py-2 px-3">
                    <Badge v-if="endpoint.role" variant="outline" class="text-xs">{{ endpoint.role }}</Badge>
                    <Badge v-else-if="endpoint.auth" variant="outline" class="text-xs">Required</Badge>
                    <span v-else class="text-xs text-muted-foreground">Public</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Users -->
    <div id="users" class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Users</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Method</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Endpoint</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Description</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Auth</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(endpoint, idx) in endpoints.users" :key="idx" class="border-b last:border-0">
                  <td class="py-2 px-3">
                    <Badge :class="getMethodColor(endpoint.method)" class="text-xs">{{ endpoint.method }}</Badge>
                  </td>
                  <td class="py-2 px-3 font-mono text-sm">{{ endpoint.path }}</td>
                  <td class="py-2 px-3 text-sm text-muted-foreground">{{ endpoint.description }}</td>
                  <td class="py-2 px-3">
                    <Badge v-if="endpoint.role" variant="outline" class="text-xs">{{ endpoint.role }}</Badge>
                    <Badge v-else-if="endpoint.auth" variant="outline" class="text-xs">Required</Badge>
                    <span v-else class="text-xs text-muted-foreground">Public</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Authentication -->
    <div id="auth" class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Authentication</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Method</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Endpoint</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Description</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Auth</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(endpoint, idx) in endpoints.auth" :key="idx" class="border-b last:border-0">
                  <td class="py-2 px-3">
                    <Badge :class="getMethodColor(endpoint.method)" class="text-xs">{{ endpoint.method }}</Badge>
                  </td>
                  <td class="py-2 px-3 font-mono text-sm">{{ endpoint.path }}</td>
                  <td class="py-2 px-3 text-sm text-muted-foreground">{{ endpoint.description }}</td>
                  <td class="py-2 px-3">
                    <Badge v-if="endpoint.auth" variant="outline" class="text-xs">Required</Badge>
                    <span v-else class="text-xs text-muted-foreground">Public</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- AI -->
    <div id="ai">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">AI Integration</h2>
      <Card>
        <CardContent class="pt-6">
          <p class="text-muted-foreground mb-4">
            AI endpoints powered by Amazon Bedrock (Claude Opus 4.5).
          </p>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Method</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Endpoint</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Description</th>
                  <th class="text-left py-2 px-3 text-sm font-medium text-muted-foreground">Auth</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(endpoint, idx) in endpoints.ai" :key="idx" class="border-b last:border-0">
                  <td class="py-2 px-3">
                    <Badge :class="getMethodColor(endpoint.method)" class="text-xs">{{ endpoint.method }}</Badge>
                  </td>
                  <td class="py-2 px-3 font-mono text-sm">{{ endpoint.path }}</td>
                  <td class="py-2 px-3 text-sm text-muted-foreground">{{ endpoint.description }}</td>
                  <td class="py-2 px-3">
                    <Badge v-if="endpoint.auth" variant="outline" class="text-xs">Required</Badge>
                    <span v-else class="text-xs text-muted-foreground">Public</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
