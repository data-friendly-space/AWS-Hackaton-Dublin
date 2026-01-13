<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'Data Models - Documentation - Resilio',
})
</script>

<template>
  <div>
    <Badge class="mb-4">Core Concepts</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">Data Models</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Complete reference for all database models and their relationships.
    </p>

    <!-- User Model -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Badge>Model</Badge>
          User
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">Custom user model with role-based access control.</p>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-cyan-400">class</span> <span class="text-yellow-400">User</span>:
    id: <span class="text-green-400">UUID</span>                <span class="text-slate-500"># Primary key</span>
    email: <span class="text-green-400">str</span>              <span class="text-slate-500"># Unique, used for login</span>
    first_name: <span class="text-green-400">str</span>
    last_name: <span class="text-green-400">str</span>
    role: <span class="text-green-400">str</span>               <span class="text-slate-500"># 'superadmin' | 'r4s_manager' | 'project_staff'</span>
    title: <span class="text-green-400">str</span>              <span class="text-slate-500"># Optional</span>
    country: <span class="text-green-400">str</span>            <span class="text-slate-500"># Optional</span>
    department: <span class="text-green-400">str</span>         <span class="text-slate-500"># Optional</span>
    job_title: <span class="text-green-400">str</span>          <span class="text-slate-500"># Optional</span>
    is_active: <span class="text-green-400">bool</span>         <span class="text-slate-500"># Account status</span>
    created_at: <span class="text-green-400">datetime</span>
    updated_at: <span class="text-green-400">datetime</span>
    last_login: <span class="text-green-400">datetime</span>    <span class="text-slate-500"># Nullable</span></pre>
        </div>
        <div class="mt-4">
          <h4 class="font-medium mb-2">Roles</h4>
          <div class="flex gap-2 flex-wrap">
            <Badge variant="outline">superadmin - Full access</Badge>
            <Badge variant="outline">r4s_manager - Project management</Badge>
            <Badge variant="outline">project_staff - View & contribute</Badge>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Project Model -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Badge>Model</Badge>
          Project
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">Container for organizing systems and team members.</p>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-cyan-400">class</span> <span class="text-yellow-400">Project</span>:
    id: <span class="text-green-400">UUID</span>
    slug: <span class="text-green-400">str</span>               <span class="text-slate-500"># URL-friendly identifier</span>
    name: <span class="text-green-400">str</span>
    description: <span class="text-green-400">str</span>
    country: <span class="text-green-400">str</span>
    start_date: <span class="text-green-400">date</span>         <span class="text-slate-500"># Optional</span>
    end_date: <span class="text-green-400">date</span>           <span class="text-slate-500"># Optional</span>
    is_active: <span class="text-green-400">bool</span>
    created_by: <span class="text-green-400">User</span>         <span class="text-slate-500"># Foreign key</span>
    members: <span class="text-green-400">List[User]</span>      <span class="text-slate-500"># Many-to-many</span>
    created_at: <span class="text-green-400">datetime</span>
    updated_at: <span class="text-green-400">datetime</span></pre>
        </div>
      </CardContent>
    </Card>

    <!-- System Model -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Badge>Model</Badge>
          System
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">Core entity representing a mapped social system.</p>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-cyan-400">class</span> <span class="text-yellow-400">System</span>:
    id: <span class="text-green-400">UUID</span>
    slug: <span class="text-green-400">str</span>               <span class="text-slate-500"># Unique URL identifier</span>
    name: <span class="text-green-400">str</span>
    description: <span class="text-green-400">str</span>
    sector: <span class="text-green-400">str</span>             <span class="text-slate-500"># Enum: health, education, market, etc.</span>
    subsector: <span class="text-green-400">str</span>          <span class="text-slate-500"># E.g., 'RMNCAH' for health</span>
    region: <span class="text-green-400">str</span>
    country: <span class="text-green-400">str</span>
    assessment_date: <span class="text-green-400">date</span>
    version: <span class="text-green-400">str</span>            <span class="text-slate-500"># E.g., '2.1'</span>
    project: <span class="text-green-400">Project</span>        <span class="text-slate-500"># Foreign key, nullable</span>
    created_by: <span class="text-green-400">User</span>        <span class="text-slate-500"># Foreign key</span>
    created_at: <span class="text-green-400">datetime</span>
    updated_at: <span class="text-green-400">datetime</span></pre>
        </div>
        <div class="mt-4">
          <h4 class="font-medium mb-2">Sector Choices</h4>
          <div class="flex gap-2 flex-wrap">
            <Badge variant="secondary">health</Badge>
            <Badge variant="secondary">education</Badge>
            <Badge variant="secondary">market</Badge>
            <Badge variant="secondary">water</Badge>
            <Badge variant="secondary">protection</Badge>
            <Badge variant="secondary">nutrition</Badge>
            <Badge variant="secondary">shelter</Badge>
            <Badge variant="secondary">livelihoods</Badge>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Actor Model -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Badge>Model</Badge>
          Actor
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">Entities within a system that provide or receive services.</p>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-cyan-400">class</span> <span class="text-yellow-400">Actor</span>:
    id: <span class="text-green-400">UUID</span>
    system: <span class="text-green-400">System</span>          <span class="text-slate-500"># Foreign key</span>
    name: <span class="text-green-400">str</span>
    slug: <span class="text-green-400">str</span>
    actor_type: <span class="text-green-400">str</span>         <span class="text-slate-500"># Enum: service_user, service_provider, support, regulatory</span>
    function: <span class="text-green-400">str</span>           <span class="text-slate-500"># Description of actor's role</span>
    position_x: <span class="text-green-400">int</span>         <span class="text-slate-500"># For diagram positioning</span>
    position_y: <span class="text-green-400">int</span>
    created_at: <span class="text-green-400">datetime</span>
    updated_at: <span class="text-green-400">datetime</span></pre>
        </div>
        <div class="mt-4">
          <h4 class="font-medium mb-2">Actor Types</h4>
          <div class="flex gap-2 flex-wrap">
            <Badge class="bg-blue-100 text-blue-700">service_user</Badge>
            <Badge class="bg-green-100 text-green-700">service_provider</Badge>
            <Badge class="bg-purple-100 text-purple-700">support</Badge>
            <Badge class="bg-orange-100 text-orange-700">regulatory</Badge>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Relationship Model -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Badge>Model</Badge>
          Relationship
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">Connections between actors showing service/goods flow.</p>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-cyan-400">class</span> <span class="text-yellow-400">Relationship</span>:
    id: <span class="text-green-400">UUID</span>
    system: <span class="text-green-400">System</span>          <span class="text-slate-500"># Foreign key</span>
    from_actor: <span class="text-green-400">Actor</span>       <span class="text-slate-500"># Foreign key - source</span>
    to_actor: <span class="text-green-400">Actor</span>         <span class="text-slate-500"># Foreign key - destination</span>
    relationship_type: <span class="text-green-400">str</span> <span class="text-slate-500"># Type classification</span>
    goods_services: <span class="text-green-400">str</span>     <span class="text-slate-500"># What is exchanged</span>
    quality: <span class="text-green-400">str</span>            <span class="text-slate-500"># Enum: good, stressed, bad, absent</span>
    created_at: <span class="text-green-400">datetime</span>
    updated_at: <span class="text-green-400">datetime</span></pre>
        </div>
        <div class="mt-4">
          <h4 class="font-medium mb-2">Quality Levels</h4>
          <div class="flex gap-2 flex-wrap">
            <Badge class="bg-green-100 text-green-700">good</Badge>
            <Badge class="bg-amber-100 text-amber-700">stressed</Badge>
            <Badge class="bg-red-100 text-red-700">bad</Badge>
            <Badge class="bg-gray-100 text-gray-700">absent</Badge>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Risk Model -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Badge>Model</Badge>
          Risk
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">Potential threats to system function.</p>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-cyan-400">class</span> <span class="text-yellow-400">Risk</span>:
    id: <span class="text-green-400">UUID</span>
    system: <span class="text-green-400">System</span>          <span class="text-slate-500"># Foreign key</span>
    name: <span class="text-green-400">str</span>
    slug: <span class="text-green-400">str</span>
    description: <span class="text-green-400">str</span>
    category: <span class="text-green-400">str</span>           <span class="text-slate-500"># Enum: climate, conflict, economic, health, political</span>
    likelihood: <span class="text-green-400">str</span>         <span class="text-slate-500"># Enum: low, medium, high</span>
    impact: <span class="text-green-400">str</span>             <span class="text-slate-500"># Enum: low, medium, high</span>
    created_at: <span class="text-green-400">datetime</span>
    updated_at: <span class="text-green-400">datetime</span></pre>
        </div>
      </CardContent>
    </Card>

    <!-- Entity Relationship Diagram -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Entity Relationships</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>
┌──────────┐       ┌──────────┐       ┌──────────┐
│   User   │──────▶│ Project  │◀──────│  System  │
└──────────┘       └──────────┘       └────┬─────┘
     │                                     │
     │ created_by                          │
     │                          ┌──────────┼──────────┐
     ▼                          ▼          ▼          ▼
┌──────────┐              ┌──────────┐ ┌──────┐ ┌──────────┐
│  System  │              │  Actor   │ │ Risk │ │Component │
└──────────┘              └────┬─────┘ └──────┘ └──────────┘
                               │
                               │ from_actor / to_actor
                               ▼
                        ┌──────────────┐
                        │ Relationship │
                        └──────────────┘</pre>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
