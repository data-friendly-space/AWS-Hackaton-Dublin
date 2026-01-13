<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'Authentication - Documentation - Resilio',
})
</script>

<template>
  <div>
    <Badge class="mb-4">Core Concepts</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">Authentication</h1>
    <p class="text-xl text-muted-foreground mb-8">
      JWT-based authentication with role-based access control.
    </p>

    <!-- Overview -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Overview</h2>
      <div class="prose prose-slate max-w-none">
        <p>
          Resilio uses <strong>JSON Web Tokens (JWT)</strong> for authentication. When a user logs in,
          they receive two tokens:
        </p>
        <ul>
          <li><strong>Access Token</strong> - Short-lived (1 hour), used for API requests</li>
          <li><strong>Refresh Token</strong> - Long-lived (7 days), used to obtain new access tokens</li>
        </ul>
      </div>
    </div>

    <!-- Login Flow -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle>Login Flow</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto mb-4">
          <pre><span class="text-slate-500"># 1. Login request</span>
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your-password"
}</pre>
        </div>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-slate-500"># Response</span>
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "superadmin",
    "role_display": "Superadmin"
  }
}</pre>
        </div>
      </CardContent>
    </Card>

    <!-- Using Access Token -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle>Making Authenticated Requests</CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">
          Include the access token in the <code>Authorization</code> header for all API requests.
        </p>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>GET /api/systems/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...</pre>
        </div>
      </CardContent>
    </Card>

    <!-- Refresh Token -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle>Refreshing Tokens</CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">
          When the access token expires, use the refresh token to obtain a new one.
        </p>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto mb-4">
          <pre>POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}</pre>
        </div>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-slate-500"># Response</span>
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}</pre>
        </div>
      </CardContent>
    </Card>

    <!-- Role-Based Access Control -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Role-Based Access Control</h2>
      <p class="text-muted-foreground mb-6">
        Three user roles with different permission levels:
      </p>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b">
              <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Permission</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Superadmin</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-muted-foreground">R4S Manager</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Project Staff</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-b">
              <td class="py-3 px-4">View all systems</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
            </tr>
            <tr class="border-b">
              <td class="py-3 px-4">Create/edit systems</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-amber-600">Project only</td>
            </tr>
            <tr class="border-b">
              <td class="py-3 px-4">Upload data to systems</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-red-600">✗</td>
            </tr>
            <tr class="border-b">
              <td class="py-3 px-4">Manage projects</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-red-600">✗</td>
            </tr>
            <tr class="border-b">
              <td class="py-3 px-4">Manage users</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-red-600">✗</td>
              <td class="py-3 px-4 text-center text-red-600">✗</td>
            </tr>
            <tr class="border-b">
              <td class="py-3 px-4">Access admin panel</td>
              <td class="py-3 px-4 text-center text-green-600">✓</td>
              <td class="py-3 px-4 text-center text-red-600">✗</td>
              <td class="py-3 px-4 text-center text-red-600">✗</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- JWT Claims -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle>JWT Token Claims</CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">
          The access token payload contains:
        </p>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>{
  "token_type": "access",
  "exp": 1768323248,           <span class="text-slate-500">// Expiration timestamp</span>
  "iat": 1768319648,           <span class="text-slate-500">// Issued at timestamp</span>
  "jti": "unique-token-id",    <span class="text-slate-500">// JWT ID</span>
  "user_id": "uuid-here",
  "email": "user@example.com",
  "role": "superadmin",
  "full_name": "John Doe"
}</pre>
        </div>
      </CardContent>
    </Card>

    <!-- Security Best Practices -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Security Best Practices</h2>
      <div class="prose prose-slate max-w-none">
        <ul>
          <li>Store tokens in <code>localStorage</code> (frontend handles this automatically)</li>
          <li>Always use HTTPS in production</li>
          <li>Access tokens expire after 1 hour - implement automatic refresh</li>
          <li>Refresh tokens expire after 7 days - users must re-login</li>
          <li>On logout, clear both tokens from storage</li>
          <li>Never expose tokens in URLs or logs</li>
        </ul>
      </div>
    </div>
  </div>
</template>
