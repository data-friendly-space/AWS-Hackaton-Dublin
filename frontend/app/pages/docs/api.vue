<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'REST API - Documentation - Resilio',
})
</script>

<template>
  <div>
    <Badge class="mb-4">API Reference</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">REST API</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Complete reference for the Resilio REST API.
    </p>

    <!-- Base URL -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle>Base URL</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="space-y-2">
          <div>
            <span class="text-sm text-muted-foreground">Production:</span>
            <code class="ml-2 bg-muted px-2 py-1 rounded">https://d18cm0umrsa2ex.cloudfront.net/api</code>
          </div>
          <div>
            <span class="text-sm text-muted-foreground">Development:</span>
            <code class="ml-2 bg-muted px-2 py-1 rounded">http://localhost:8000/api</code>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Authentication -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Authentication Headers</h2>
      <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
        <pre>Authorization: Bearer &lt;access_token&gt;
Content-Type: application/json</pre>
      </div>
    </div>

    <!-- Auth Endpoints -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Authentication Endpoints</h2>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Badge class="bg-green-600">POST</Badge>
            /api/auth/login/
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">Authenticate user and receive JWT tokens.</p>
          <h4 class="font-medium mb-2">Request Body</h4>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto mb-4">
            <pre>{
  "email": "user@example.com",
  "password": "your-password"
}</pre>
          </div>
          <h4 class="font-medium mb-2">Response (200)</h4>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "superadmin"
  }
}</pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Badge class="bg-green-600">POST</Badge>
            /api/auth/refresh/
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">Refresh access token using refresh token.</p>
          <h4 class="font-medium mb-2">Request Body</h4>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto mb-4">
            <pre>{ "refresh": "eyJ..." }</pre>
          </div>
          <h4 class="font-medium mb-2">Response (200)</h4>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>{ "access": "eyJ..." }</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- User Endpoints -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">User Endpoints</h2>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Badge class="bg-blue-600">GET</Badge>
            /api/users/me/
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">Get current authenticated user's profile.</p>
          <Badge variant="outline" class="mb-4">Requires Authentication</Badge>
          <h4 class="font-medium mb-2">Response (200)</h4>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "role": "superadmin",
  "role_display": "Superadmin",
  "is_active": true
}</pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Badge class="bg-amber-600">PATCH</Badge>
            /api/users/me/
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">Update current user's profile.</p>
          <Badge variant="outline" class="mb-4">Requires Authentication</Badge>
          <h4 class="font-medium mb-2">Request Body (partial update)</h4>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>{
  "first_name": "Jane",
  "country": "Ethiopia"
}</pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Badge class="bg-blue-600">GET</Badge>
            /api/users/
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">List all users (admin only).</p>
          <Badge variant="outline" class="mb-4">Superadmin Only</Badge>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Badge class="bg-green-600">POST</Badge>
            /api/users/change_password/
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">Change current user's password.</p>
          <h4 class="font-medium mb-2">Request Body</h4>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>{
  "old_password": "current-password",
  "new_password": "new-password",
  "new_password_confirm": "new-password"
}</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- System Endpoints -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">System Endpoints</h2>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Badge class="bg-blue-600">GET</Badge>
            /api/systems/
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">List all systems with pagination.</p>
          <h4 class="font-medium mb-2">Query Parameters</h4>
          <div class="space-y-2 mb-4">
            <div><code class="bg-muted px-1 rounded">sector</code> - Filter by sector</div>
            <div><code class="bg-muted px-1 rounded">country</code> - Filter by country</div>
            <div><code class="bg-muted px-1 rounded">page</code> - Page number</div>
          </div>
          <h4 class="font-medium mb-2">Response (200)</h4>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>{
  "count": 10,
  "next": "/api/systems/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "slug": "rmncah-eastern-ethiopia",
      "name": "RMNCAH Health System",
      "sector": "health",
      "sector_display": "Health",
      "actor_count": 12,
      "risk_count": 5
    }
  ]
}</pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Badge class="bg-blue-600">GET</Badge>
            /api/systems/{slug}/
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">Get system details including actors, relationships, and risks.</p>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Badge class="bg-green-600">POST</Badge>
            /api/systems/
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">Create a new system.</p>
          <h4 class="font-medium mb-2">Request Body</h4>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>{
  "name": "Health System - Region X",
  "description": "Description here",
  "sector": "health",
  "subsector": "RMNCAH",
  "region": "Eastern",
  "country": "Ethiopia"
}</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Other Endpoints -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Other Endpoints</h2>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b">
              <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Method</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Endpoint</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-b">
              <td class="py-3 px-4"><Badge class="bg-blue-600">GET</Badge></td>
              <td class="py-3 px-4 font-mono text-sm">/api/actors/</td>
              <td class="py-3 px-4 text-muted-foreground">List actors</td>
            </tr>
            <tr class="border-b">
              <td class="py-3 px-4"><Badge class="bg-blue-600">GET</Badge></td>
              <td class="py-3 px-4 font-mono text-sm">/api/relationships/</td>
              <td class="py-3 px-4 text-muted-foreground">List relationships</td>
            </tr>
            <tr class="border-b">
              <td class="py-3 px-4"><Badge class="bg-blue-600">GET</Badge></td>
              <td class="py-3 px-4 font-mono text-sm">/api/risks/</td>
              <td class="py-3 px-4 text-muted-foreground">List risk scenarios</td>
            </tr>
            <tr class="border-b">
              <td class="py-3 px-4"><Badge class="bg-blue-600">GET</Badge></td>
              <td class="py-3 px-4 font-mono text-sm">/api/projects/</td>
              <td class="py-3 px-4 text-muted-foreground">List projects</td>
            </tr>
            <tr class="border-b">
              <td class="py-3 px-4"><Badge class="bg-blue-600">GET</Badge></td>
              <td class="py-3 px-4 font-mono text-sm">/api/health/</td>
              <td class="py-3 px-4 text-muted-foreground">Health check endpoint</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Error Responses -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Error Responses</h2>
      <div class="space-y-4">
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3 mb-2">
              <Badge variant="destructive">401</Badge>
              <span class="font-medium">Unauthorized</span>
            </div>
            <p class="text-sm text-muted-foreground">Missing or invalid authentication token</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3 mb-2">
              <Badge variant="destructive">403</Badge>
              <span class="font-medium">Forbidden</span>
            </div>
            <p class="text-sm text-muted-foreground">Insufficient permissions for this action</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3 mb-2">
              <Badge variant="destructive">404</Badge>
              <span class="font-medium">Not Found</span>
            </div>
            <p class="text-sm text-muted-foreground">Resource does not exist</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3 mb-2">
              <Badge variant="destructive">400</Badge>
              <span class="font-medium">Bad Request</span>
            </div>
            <p class="text-sm text-muted-foreground">Invalid request body or parameters</p>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>
