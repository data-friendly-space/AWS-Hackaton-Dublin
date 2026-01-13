<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { CheckCircle2 } from 'lucide-vue-next'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'Quick Start - Documentation - Resilio',
})
</script>

<template>
  <div>
    <Badge class="mb-4">Getting Started</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">Quick Start Guide</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Get Resilio up and running locally in under 10 minutes.
    </p>

    <!-- Prerequisites -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Prerequisites</h2>
      <div class="grid gap-3 md:grid-cols-2">
        <div class="flex items-center gap-3 p-3 rounded-lg border">
          <CheckCircle2 class="h-5 w-5 text-green-500" />
          <span>Node.js 20+</span>
        </div>
        <div class="flex items-center gap-3 p-3 rounded-lg border">
          <CheckCircle2 class="h-5 w-5 text-green-500" />
          <span>Python 3.12+</span>
        </div>
        <div class="flex items-center gap-3 p-3 rounded-lg border">
          <CheckCircle2 class="h-5 w-5 text-green-500" />
          <span>Docker Desktop</span>
        </div>
        <div class="flex items-center gap-3 p-3 rounded-lg border">
          <CheckCircle2 class="h-5 w-5 text-green-500" />
          <span>AWS CLI (for deployment)</span>
        </div>
      </div>
    </div>

    <!-- Backend Setup -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <span class="flex h-6 w-6 items-center justify-center rounded-full bg-goal text-white text-sm">1</span>
          Backend Setup
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-slate-500"># Navigate to backend directory</span>
cd backend

<span class="text-slate-500"># Create virtual environment</span>
python -m venv venv
source venv/bin/activate  <span class="text-slate-500"># Windows: venv\Scripts\activate</span>

<span class="text-slate-500"># Install dependencies</span>
pip install -r requirements.txt

<span class="text-slate-500"># Run database migrations</span>
python manage.py migrate

<span class="text-slate-500"># Create superuser account</span>
python manage.py createsuperuser

<span class="text-slate-500"># Start development server</span>
python manage.py runserver</pre>
        </div>
        <p class="text-sm text-muted-foreground mt-3">
          The backend will be available at <code class="bg-muted px-1 py-0.5 rounded">http://localhost:8000</code>
        </p>
      </CardContent>
    </Card>

    <!-- Frontend Setup -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <span class="flex h-6 w-6 items-center justify-center rounded-full bg-goal text-white text-sm">2</span>
          Frontend Setup
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre><span class="text-slate-500"># Navigate to frontend directory</span>
cd frontend

<span class="text-slate-500"># Install dependencies</span>
npm install

<span class="text-slate-500"># Start development server</span>
npm run dev</pre>
        </div>
        <p class="text-sm text-muted-foreground mt-3">
          The frontend will be available at <code class="bg-muted px-1 py-0.5 rounded">http://localhost:3000</code>
        </p>
      </CardContent>
    </Card>

    <!-- Environment Variables -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <span class="flex h-6 w-6 items-center justify-center rounded-full bg-goal text-white text-sm">3</span>
          Environment Configuration
        </CardTitle>
      </CardHeader>
      <CardContent>
        <h4 class="font-medium mb-2">Backend (.env)</h4>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto mb-4">
          <pre>DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

<span class="text-slate-500"># Production database (optional)</span>
DB_HOST=
DB_NAME=resilio
DB_USER=
DB_PASSWORD=
DB_PORT=5432</pre>
        </div>

        <h4 class="font-medium mb-2">Frontend (nuxt.config.ts)</h4>
        <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>runtimeConfig: {
  public: {
    <span class="text-slate-500">// Uses relative URL for CloudFront proxy</span>
    apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api',
  },
}</pre>
        </div>
      </CardContent>
    </Card>

    <!-- Login -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <span class="flex h-6 w-6 items-center justify-center rounded-full bg-goal text-white text-sm">4</span>
          First Login
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ol class="space-y-3 text-muted-foreground">
          <li>1. Navigate to <code class="bg-muted px-1 py-0.5 rounded">http://localhost:3000/login</code></li>
          <li>2. Enter the superuser credentials you created</li>
          <li>3. You'll be redirected to the Systems page</li>
          <li>4. Explore the mock data or create your own systems</li>
        </ol>
      </CardContent>
    </Card>

    <!-- Next Steps -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Next Steps</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <NuxtLink to="/docs/systems" class="block">
          <Card class="h-full hover:border-goal/30 transition-colors cursor-pointer">
            <CardContent class="pt-6">
              <h3 class="font-semibold mb-1">Learn Core Concepts</h3>
              <p class="text-sm text-muted-foreground">Understand systems, actors, and relationships</p>
            </CardContent>
          </Card>
        </NuxtLink>
        <NuxtLink to="/docs/api" class="block">
          <Card class="h-full hover:border-goal/30 transition-colors cursor-pointer">
            <CardContent class="pt-6">
              <h3 class="font-semibold mb-1">Explore the API</h3>
              <p class="text-sm text-muted-foreground">View all available endpoints</p>
            </CardContent>
          </Card>
        </NuxtLink>
        <NuxtLink to="/docs/aws" class="block">
          <Card class="h-full hover:border-goal/30 transition-colors cursor-pointer">
            <CardContent class="pt-6">
              <h3 class="font-semibold mb-1">Deploy to AWS</h3>
              <p class="text-sm text-muted-foreground">Set up production infrastructure</p>
            </CardContent>
          </Card>
        </NuxtLink>
        <NuxtLink to="/systems" class="block">
          <Card class="h-full hover:border-goal/30 transition-colors cursor-pointer">
            <CardContent class="pt-6">
              <h3 class="font-semibold mb-1">View Demo Systems</h3>
              <p class="text-sm text-muted-foreground">Explore mock R4S systems</p>
            </CardContent>
          </Card>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
