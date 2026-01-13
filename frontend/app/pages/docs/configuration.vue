<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'Configuration - Documentation - Resilio',
})
</script>

<template>
  <div>
    <Badge class="mb-4">Deployment</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">Configuration</h1>
    <p class="text-xl text-muted-foreground mb-8">
      Complete reference for all configuration options in Resilio.
    </p>

    <!-- Backend Configuration -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Backend Configuration</h2>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle>Django Settings</CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">
            Configure the backend via environment variables or <code class="bg-muted px-1 rounded">.env</code> file in the backend directory.
          </p>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-slate-500"># Core Settings</span>
DEBUG=True                          <span class="text-slate-500"># Set False in production</span>
SECRET_KEY=your-secret-key          <span class="text-slate-500"># Required, generate a secure key</span>
ALLOWED_HOSTS=localhost,127.0.0.1   <span class="text-slate-500"># Comma-separated hostnames</span>

<span class="text-slate-500"># Database</span>
DB_ENGINE=django.db.backends.postgresql
DB_HOST=localhost                   <span class="text-slate-500"># RDS endpoint in production</span>
DB_NAME=resilio
DB_USER=postgres
DB_PASSWORD=your-password
DB_PORT=5432

<span class="text-slate-500"># JWT Settings</span>
JWT_ACCESS_TOKEN_LIFETIME=60        <span class="text-slate-500"># Minutes</span>
JWT_REFRESH_TOKEN_LIFETIME=10080    <span class="text-slate-500"># Minutes (7 days)</span>

<span class="text-slate-500"># AWS Settings</span>
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL=anthropic.claude-opus-4-5-20250514-v1:0

<span class="text-slate-500"># CORS Settings</span>
CORS_ALLOWED_ORIGINS=http://localhost:3000
CORS_ALLOW_CREDENTIALS=True</pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle>Database Options</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div>
              <h4 class="font-medium mb-2">SQLite (Development)</h4>
              <p class="text-sm text-muted-foreground mb-2">Default for local development, no additional configuration needed.</p>
              <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                <pre>DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3</pre>
              </div>
            </div>
            <div>
              <h4 class="font-medium mb-2">PostgreSQL (Production)</h4>
              <p class="text-sm text-muted-foreground mb-2">Recommended for production deployments.</p>
              <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                <pre>DB_ENGINE=django.db.backends.postgresql
DB_HOST=your-rds-endpoint.amazonaws.com
DB_NAME=resilio
DB_USER=your-username
DB_PASSWORD=your-secure-password
DB_PORT=5432</pre>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Frontend Configuration -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Frontend Configuration</h2>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle>Nuxt Configuration</CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">
            Configure in <code class="bg-muted px-1 rounded">nuxt.config.ts</code> or via environment variables.
          </p>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-cyan-400">export default</span> defineNuxtConfig({
  runtimeConfig: {
    <span class="text-green-400">public</span>: {
      <span class="text-slate-500">// API base URL</span>
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api',

      <span class="text-slate-500">// App name</span>
      appName: 'Resilio',

      <span class="text-slate-500">// Feature flags</span>
      enableAI: true,
      enableExport: true,
    }
  }
})</pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle>Environment Variables</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-2 text-sm font-medium text-muted-foreground">Variable</th>
                  <th class="text-left py-2 text-sm font-medium text-muted-foreground">Default</th>
                  <th class="text-left py-2 text-sm font-medium text-muted-foreground">Description</th>
                </tr>
              </thead>
              <tbody class="text-sm">
                <tr class="border-b">
                  <td class="py-2 font-mono">NUXT_PUBLIC_API_BASE</td>
                  <td class="py-2"><code class="bg-muted px-1 rounded">/api</code></td>
                  <td class="py-2 text-muted-foreground">Base URL for API requests</td>
                </tr>
                <tr class="border-b">
                  <td class="py-2 font-mono">NODE_ENV</td>
                  <td class="py-2"><code class="bg-muted px-1 rounded">development</code></td>
                  <td class="py-2 text-muted-foreground">Environment mode</td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Authentication Configuration -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Authentication Configuration</h2>

      <Card>
        <CardHeader>
          <CardTitle>JWT Settings</CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">
            Configure in <code class="bg-muted px-1 rounded">backend/core/settings.py</code>
          </p>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>SIMPLE_JWT = {
    <span class="text-green-400">'ACCESS_TOKEN_LIFETIME'</span>: timedelta(minutes=60),
    <span class="text-green-400">'REFRESH_TOKEN_LIFETIME'</span>: timedelta(days=7),
    <span class="text-green-400">'ROTATE_REFRESH_TOKENS'</span>: False,
    <span class="text-green-400">'BLACKLIST_AFTER_ROTATION'</span>: True,
    <span class="text-green-400">'UPDATE_LAST_LOGIN'</span>: True,

    <span class="text-green-400">'ALGORITHM'</span>: 'HS256',
    <span class="text-green-400">'SIGNING_KEY'</span>: SECRET_KEY,

    <span class="text-green-400">'AUTH_HEADER_TYPES'</span>: ('Bearer',),
    <span class="text-green-400">'AUTH_HEADER_NAME'</span>: 'HTTP_AUTHORIZATION',

    <span class="text-green-400">'USER_ID_FIELD'</span>: 'id',
    <span class="text-green-400">'USER_ID_CLAIM'</span>: 'user_id',
}</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- AI Configuration -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">AI Configuration</h2>

      <Card>
        <CardHeader>
          <CardTitle>Amazon Bedrock Settings</CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">
            Configure AI model and parameters for system analysis.
          </p>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-slate-500"># Environment variables</span>
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL=anthropic.claude-opus-4-5-20250514-v1:0

<span class="text-slate-500"># Python configuration</span>
BEDROCK_CONFIG = {
    <span class="text-green-400">'model_id'</span>: 'anthropic.claude-opus-4-5-20250514-v1:0',
    <span class="text-green-400">'max_tokens'</span>: 4096,
    <span class="text-green-400">'temperature'</span>: 0.7,
    <span class="text-green-400">'top_p'</span>: 0.9,
}</pre>
          </div>
          <div class="mt-4 space-y-2">
            <h4 class="font-medium">Available Models</h4>
            <div class="flex flex-wrap gap-2">
              <Badge variant="outline">anthropic.claude-opus-4-5-20250514-v1:0</Badge>
              <Badge variant="outline">anthropic.claude-sonnet-4-20250514-v1:0</Badge>
              <Badge variant="outline">anthropic.claude-3-haiku-20240307-v1:0</Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- CORS Configuration -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">CORS Configuration</h2>

      <Card>
        <CardContent class="pt-6">
          <p class="text-muted-foreground mb-4">
            Configure Cross-Origin Resource Sharing for frontend-backend communication.
          </p>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-slate-500"># settings.py</span>
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-cloudfront-domain.cloudfront.net",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "origin",
    "x-csrftoken",
    "x-requested-with",
]</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Logging Configuration -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Logging Configuration</h2>

      <Card>
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre>LOGGING = {
    <span class="text-green-400">'version'</span>: 1,
    <span class="text-green-400">'disable_existing_loggers'</span>: False,
    <span class="text-green-400">'formatters'</span>: {
        <span class="text-green-400">'verbose'</span>: {
            <span class="text-green-400">'format'</span>: '{levelname} {asctime} {module} {message}',
            <span class="text-green-400">'style'</span>: '{',
        },
    },
    <span class="text-green-400">'handlers'</span>: {
        <span class="text-green-400">'console'</span>: {
            <span class="text-green-400">'class'</span>: 'logging.StreamHandler',
            <span class="text-green-400">'formatter'</span>: 'verbose',
        },
    },
    <span class="text-green-400">'root'</span>: {
        <span class="text-green-400">'handlers'</span>: ['console'],
        <span class="text-green-400">'level'</span>: 'INFO',
    },
    <span class="text-green-400">'loggers'</span>: {
        <span class="text-green-400">'django'</span>: {
            <span class="text-green-400">'handlers'</span>: ['console'],
            <span class="text-green-400">'level'</span>: os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            <span class="text-green-400">'propagate'</span>: False,
        },
    },
}</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Security Settings -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Security Settings</h2>

      <Card>
        <CardHeader>
          <CardTitle>Production Security Checklist</CardTitle>
        </CardHeader>
        <CardContent>
          <ul class="space-y-3">
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="bg-red-50 text-red-700 border-red-200">Required</Badge>
              <div>
                <p class="font-medium">DEBUG = False</p>
                <p class="text-sm text-muted-foreground">Never run with DEBUG=True in production</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="bg-red-50 text-red-700 border-red-200">Required</Badge>
              <div>
                <p class="font-medium">SECRET_KEY</p>
                <p class="text-sm text-muted-foreground">Use a strong, unique secret key (50+ random characters)</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="bg-red-50 text-red-700 border-red-200">Required</Badge>
              <div>
                <p class="font-medium">ALLOWED_HOSTS</p>
                <p class="text-sm text-muted-foreground">Set to your actual domain names only</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="bg-amber-50 text-amber-700 border-amber-200">Recommended</Badge>
              <div>
                <p class="font-medium">HTTPS Only</p>
                <p class="text-sm text-muted-foreground">Configure SECURE_SSL_REDIRECT = True</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="bg-amber-50 text-amber-700 border-amber-200">Recommended</Badge>
              <div>
                <p class="font-medium">HSTS Headers</p>
                <p class="text-sm text-muted-foreground">Enable SECURE_HSTS_SECONDS for strict transport security</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <Badge variant="outline" class="bg-amber-50 text-amber-700 border-amber-200">Recommended</Badge>
              <div>
                <p class="font-medium">Database Encryption</p>
                <p class="text-sm text-muted-foreground">Use RDS encryption at rest and SSL connections</p>
              </div>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
