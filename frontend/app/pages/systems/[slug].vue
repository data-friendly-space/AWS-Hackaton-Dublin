<script setup lang="ts">
import {
  ArrowLeft, Download, Network, Users, AlertTriangle, Link, Bot,
  Send, Sparkles, Component, FileText, Eye, MessageSquare,
  ChevronRight, Info, CheckCircle2, XCircle, AlertCircle
} from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'

const route = useRoute()
const slug = route.params.slug as string

const { getSystemBySlug } = useMockSystems()
const system = getSystemBySlug(slug)

useHead({
  title: () => system ? `${system.name} - Resilio` : 'System Not Found',
})

// Chat state
const chatInput = ref('')
const chatMessages = ref<Array<{ role: 'user' | 'assistant'; content: string }>>([
  {
    role: 'assistant',
    content: `Hello! I'm your AI assistant for analyzing the **${system?.name || 'system'}**. I can help you understand:

- System vulnerabilities and resilience factors
- Actor relationships and dependencies
- Risk scenarios and mitigation strategies
- Component status and recommendations

What would you like to know about this system?`
  }
])
const isTyping = ref(false)

async function sendMessage() {
  if (!chatInput.value.trim()) return

  const userMessage = chatInput.value
  chatMessages.value.push({ role: 'user', content: userMessage })
  chatInput.value = ''
  isTyping.value = true

  // Simulate AI response (in production, this would call Bedrock)
  await new Promise(resolve => setTimeout(resolve, 1500))

  let response = ''
  const lowerMessage = userMessage.toLowerCase()

  if (lowerMessage.includes('vulnerab') || lowerMessage.includes('risk')) {
    response = `Based on my analysis of the ${system?.name}, the key vulnerabilities are:

1. **Supply Chain Dependency** (High Risk): The system heavily relies on the Regional Health Bureau for pharmaceutical supplies, creating a single point of failure.

2. **Climate Exposure** (High): 60% of service areas are affected by recurring droughts, impacting both service delivery and demand.

3. **Infrastructure Gaps** (Medium): Health facilities experience frequent power outages, affecting cold chain integrity.

**Recommended Actions:**
- Establish buffer stock mechanisms at zonal level
- Invest in solar power for critical facilities
- Diversify supply sources through NGO partnerships`
  } else if (lowerMessage.includes('actor') || lowerMessage.includes('relationship')) {
    response = `The system has **${system?.actor_count} actors** across 4 categories:

**Service Users (2):**
- Pregnant Women & Mothers - High vulnerability
- Children Under 5 - High vulnerability

**Service Providers (5):**
- Health Centers, HEWs, Traditional Birth Attendants, Private Pharmacies, Zonal Hospital

**Support Actors (3):**
- GOAL Ethiopia, UNICEF, Community Leaders

**Regulatory (2):**
- Woreda Health Office, Regional Health Bureau

The most critical relationships are between Health Centers and the Regional Health Bureau (supply chain) and between HEWs and community members (service delivery).`
  } else if (lowerMessage.includes('recommend') || lowerMessage.includes('improve')) {
    response = `Based on the R4S assessment, here are my top recommendations for strengthening this system:

1. **Short-term (0-3 months):**
   - Formalize coordination protocols between government and NGO actors
   - Establish emergency communication channels

2. **Medium-term (3-12 months):**
   - Build buffer stock mechanisms at zonal level
   - Train additional Health Extension Workers

3. **Long-term (1-3 years):**
   - Invest in solar power systems for all health facilities
   - Develop community-based health financing mechanisms

Would you like me to elaborate on any of these recommendations?`
  } else {
    response = `That's a great question about the ${system?.name}.

This system serves approximately 2.3 million people across 12 woredas in Eastern Ethiopia. The current resilience score is **${system?.resilience_score}%**, which indicates moderate resilience with room for improvement.

Key strengths include strong community health worker networks and effective NGO partnerships. Main challenges are supply chain reliability and infrastructure maintenance.

Is there a specific aspect you'd like me to analyze in more detail?`
  }

  chatMessages.value.push({ role: 'assistant', content: response })
  isTyping.value = false
}

// Actor type colors
const actorTypeColors: Record<string, string> = {
  service_user: 'bg-blue-100 text-blue-700 border-blue-300',
  service_provider: 'bg-green-100 text-green-700 border-green-300',
  support: 'bg-purple-100 text-purple-700 border-purple-300',
  regulatory: 'bg-orange-100 text-orange-700 border-orange-300',
}

// Quality colors
const qualityColors: Record<string, string> = {
  good: 'bg-green-100 text-green-700',
  stressed: 'bg-amber-100 text-amber-700',
  bad: 'bg-red-100 text-red-700',
  absent: 'bg-gray-100 text-gray-700',
}

// Component status colors
const statusColors: Record<string, string> = {
  functional: 'bg-green-100 text-green-700',
  degraded: 'bg-amber-100 text-amber-700',
  non_functional: 'bg-red-100 text-red-700',
}

const statusIcons: Record<string, any> = {
  functional: CheckCircle2,
  degraded: AlertCircle,
  non_functional: XCircle,
}

// Category colors for components
const categoryColors: Record<string, string> = {
  infrastructure: 'bg-slate-100 text-slate-700',
  human_resource: 'bg-blue-100 text-blue-700',
  financial: 'bg-emerald-100 text-emerald-700',
  information: 'bg-cyan-100 text-cyan-700',
  governance: 'bg-violet-100 text-violet-700',
}
</script>

<template>
  <div class="container py-8">
    <div v-if="!system" class="text-center py-16">
      <p class="text-destructive">System not found</p>
      <Button variant="outline" class="mt-4" as-child>
        <NuxtLink to="/systems">
          <ArrowLeft class="mr-2 h-4 w-4" />
          Back to Systems
        </NuxtLink>
      </Button>
    </div>

    <template v-else>
      <!-- Header -->
      <div class="mb-8">
        <NuxtLink to="/systems" class="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-4">
          <ArrowLeft class="mr-1 h-4 w-4" />
          Back to Systems
        </NuxtLink>

        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-3xl font-bold text-goal-dark">{{ system.name }}</h1>
            <p class="text-muted-foreground mt-1 max-w-2xl">
              {{ system.description }}
            </p>
            <div class="flex flex-wrap gap-2 mt-3">
              <Badge variant="default">{{ system.sector_display }}</Badge>
              <Badge v-if="system.subsector" variant="secondary">{{ system.subsector }}</Badge>
              <Badge v-if="system.region" variant="outline">{{ system.region }}</Badge>
              <Badge v-if="system.country" variant="outline">{{ system.country }}</Badge>
            </div>
          </div>
          <Button variant="outline">
            <Download class="mr-2 h-4 w-4" />
            Export Report
          </Button>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-2 sm:grid-cols-5 gap-4 mb-8">
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
                <Users class="h-5 w-5 text-goal" />
              </div>
              <div>
                <div class="text-2xl font-bold">{{ system.actor_count }}</div>
                <div class="text-sm text-muted-foreground">Actors</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
                <Link class="h-5 w-5 text-goal" />
              </div>
              <div>
                <div class="text-2xl font-bold">{{ system.relationship_count }}</div>
                <div class="text-sm text-muted-foreground">Relationships</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
                <Component class="h-5 w-5 text-goal" />
              </div>
              <div>
                <div class="text-2xl font-bold">{{ system.component_count }}</div>
                <div class="text-sm text-muted-foreground">Components</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
                <AlertTriangle class="h-5 w-5 text-goal" />
              </div>
              <div>
                <div class="text-2xl font-bold">{{ system.risk_count }}</div>
                <div class="text-sm text-muted-foreground">Risk Scenarios</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-goal/10">
                <Network class="h-5 w-5 text-goal" />
              </div>
              <div>
                <div class="text-2xl font-bold">{{ system.resilience_score }}%</div>
                <div class="text-sm text-muted-foreground">Resilience</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Main Content Tabs -->
      <Tabs default-value="summary" class="w-full">
        <TabsList class="grid w-full grid-cols-4 lg:w-auto lg:inline-grid">
          <TabsTrigger value="summary" class="gap-2">
            <Sparkles class="h-4 w-4" />
            <span class="hidden sm:inline">AI Summary</span>
            <span class="sm:hidden">Summary</span>
          </TabsTrigger>
          <TabsTrigger value="visualization" class="gap-2">
            <Eye class="h-4 w-4" />
            <span class="hidden sm:inline">Visualization</span>
            <span class="sm:hidden">Visual</span>
          </TabsTrigger>
          <TabsTrigger value="components" class="gap-2">
            <Component class="h-4 w-4" />
            <span class="hidden sm:inline">Components</span>
            <span class="sm:hidden">Data</span>
          </TabsTrigger>
          <TabsTrigger value="chat" class="gap-2">
            <MessageSquare class="h-4 w-4" />
            <span class="hidden sm:inline">AI Chat</span>
            <span class="sm:hidden">Chat</span>
          </TabsTrigger>
        </TabsList>

        <!-- AI Summary Tab -->
        <TabsContent value="summary" class="mt-6">
          <div class="grid gap-6 lg:grid-cols-3">
            <!-- Main Summary -->
            <Card class="lg:col-span-2">
              <CardHeader>
                <div class="flex items-center gap-2">
                  <Sparkles class="h-5 w-5 text-goal" />
                  <CardTitle>AI-Generated Analysis</CardTitle>
                </div>
                <CardDescription>
                  Powered by Claude Opus 4.5 via Amazon Bedrock
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div class="prose prose-sm max-w-none dark:prose-invert" v-html="system.ai_summary.replace(/\n/g, '<br>').replace(/## /g, '<h3 class=\'text-lg font-semibold mt-6 mb-3\'>').replace(/### /g, '<h4 class=\'text-md font-medium mt-4 mb-2\'>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/- /g, '&bull; ')"></div>
              </CardContent>
            </Card>

            <!-- Side Panel -->
            <div class="space-y-6">
              <!-- Resilience Score -->
              <Card>
                <CardHeader class="pb-3">
                  <CardTitle class="text-base">Resilience Score</CardTitle>
                </CardHeader>
                <CardContent>
                  <div class="text-center mb-4">
                    <div class="text-5xl font-bold text-goal">{{ system.resilience_score }}%</div>
                    <div class="text-sm text-muted-foreground mt-1">Moderate Resilience</div>
                  </div>
                  <Progress :model-value="system.resilience_score" class="h-3" />
                  <div class="flex justify-between text-xs text-muted-foreground mt-2">
                    <span>Weak</span>
                    <span>Strong</span>
                  </div>
                </CardContent>
              </Card>

              <!-- Key Risks -->
              <Card>
                <CardHeader class="pb-3">
                  <CardTitle class="text-base">Top Risks</CardTitle>
                </CardHeader>
                <CardContent>
                  <div class="space-y-3">
                    <div v-for="risk in system.risks.slice(0, 3)" :key="risk.id" class="flex items-start gap-3">
                      <AlertTriangle :class="['h-4 w-4 mt-0.5 shrink-0', risk.likelihood === 'high' ? 'text-red-500' : 'text-amber-500']" />
                      <div>
                        <div class="text-sm font-medium">{{ risk.name }}</div>
                        <div class="text-xs text-muted-foreground">{{ risk.category_display }} - {{ risk.likelihood_display }} likelihood</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <!-- Quick Stats -->
              <Card>
                <CardHeader class="pb-3">
                  <CardTitle class="text-base">Assessment Info</CardTitle>
                </CardHeader>
                <CardContent>
                  <div class="space-y-3 text-sm">
                    <div class="flex justify-between">
                      <span class="text-muted-foreground">Version</span>
                      <span class="font-medium">{{ system.version }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-muted-foreground">Last Updated</span>
                      <span class="font-medium">{{ new Date(system.assessment_date).toLocaleDateString() }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-muted-foreground">Sector</span>
                      <span class="font-medium">{{ system.sector_display }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-muted-foreground">Location</span>
                      <span class="font-medium">{{ system.region }}, {{ system.country }}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <!-- Visualization Tab -->
        <TabsContent value="visualization" class="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>System Map</CardTitle>
              <CardDescription>
                Interactive visualization of actors, relationships, and system components
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div class="relative rounded-xl border bg-white overflow-hidden">
                <div class="absolute top-0 left-0 right-0 h-10 bg-muted/50 flex items-center px-4 gap-2">
                  <div class="w-3 h-3 rounded-full bg-red-400" />
                  <div class="w-3 h-3 rounded-full bg-yellow-400" />
                  <div class="w-3 h-3 rounded-full bg-green-400" />
                  <span class="ml-4 text-xs text-muted-foreground font-medium">{{ system.name }}</span>
                </div>
                <div class="pt-10">
                  <img
                    src="/images/system-diagram.svg"
                    alt="System Diagram"
                    class="w-full"
                  />
                </div>
              </div>

              <!-- Legend -->
              <div class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded bg-blue-100 border-2 border-blue-300"></div>
                  <span class="text-sm">Service User</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded bg-green-100 border-2 border-green-500"></div>
                  <span class="text-sm">Service Provider</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded bg-purple-100 border-2 border-purple-400"></div>
                  <span class="text-sm">Support</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded bg-orange-100 border-2 border-orange-400"></div>
                  <span class="text-sm">Regulatory</span>
                </div>
              </div>

              <!-- Actors List -->
              <div class="mt-8">
                <h3 class="text-lg font-semibold mb-4">Actors ({{ system.actors.length }})</h3>
                <div class="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
                  <div
                    v-for="actor in system.actors"
                    :key="actor.id"
                    :class="['rounded-lg border-2 p-4 transition-colors hover:shadow-md', actorTypeColors[actor.actor_type]]"
                  >
                    <div class="flex items-start justify-between mb-2">
                      <h4 class="font-medium">{{ actor.name }}</h4>
                    </div>
                    <p class="text-sm opacity-80 line-clamp-2">{{ actor.function }}</p>
                    <div class="mt-2 flex gap-2">
                      <Badge variant="outline" class="text-xs">{{ actor.actor_type_display }}</Badge>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Relationships -->
              <div class="mt-8">
                <h3 class="text-lg font-semibold mb-4">Relationships ({{ system.relationships.length }})</h3>
                <div class="space-y-3">
                  <div
                    v-for="rel in system.relationships"
                    :key="rel.id"
                    class="flex items-center justify-between rounded-lg border p-4 hover:bg-muted/50 transition-colors"
                  >
                    <div class="flex items-center gap-3 flex-1">
                      <span class="font-medium text-sm">{{ rel.from_actor_name }}</span>
                      <ChevronRight class="h-4 w-4 text-muted-foreground shrink-0" />
                      <span class="font-medium text-sm">{{ rel.to_actor_name }}</span>
                    </div>
                    <div class="flex items-center gap-3">
                      <span class="text-sm text-muted-foreground hidden md:inline">{{ rel.goods_services }}</span>
                      <Badge :class="qualityColors[rel.quality]">
                        {{ rel.quality_display }}
                      </Badge>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <!-- Components Tab -->
        <TabsContent value="components" class="mt-6">
          <div class="grid gap-6 lg:grid-cols-3">
            <div class="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>System Components</CardTitle>
                  <CardDescription>
                    Infrastructure, resources, and governance elements
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="overflow-x-auto">
                    <table class="w-full">
                      <thead>
                        <tr class="border-b">
                          <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Component</th>
                          <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Category</th>
                          <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Status</th>
                          <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground hidden md:table-cell">Dependencies</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="component in system.components" :key="component.id" class="border-b last:border-0 hover:bg-muted/50">
                          <td class="py-3 px-4">
                            <div>
                              <div class="font-medium text-sm">{{ component.name }}</div>
                              <div class="text-xs text-muted-foreground line-clamp-1">{{ component.description }}</div>
                            </div>
                          </td>
                          <td class="py-3 px-4">
                            <Badge :class="categoryColors[component.category]" variant="secondary">
                              {{ component.category_display }}
                            </Badge>
                          </td>
                          <td class="py-3 px-4">
                            <div class="flex items-center gap-2">
                              <component :is="statusIcons[component.status]" :class="['h-4 w-4', component.status === 'functional' ? 'text-green-500' : component.status === 'degraded' ? 'text-amber-500' : 'text-red-500']" />
                              <Badge :class="statusColors[component.status]">
                                {{ component.status_display }}
                              </Badge>
                            </div>
                          </td>
                          <td class="py-3 px-4 hidden md:table-cell">
                            <div class="flex flex-wrap gap-1">
                              <Badge v-for="dep in component.dependencies.slice(0, 2)" :key="dep" variant="outline" class="text-xs">
                                {{ dep }}
                              </Badge>
                              <Badge v-if="component.dependencies.length > 2" variant="outline" class="text-xs">
                                +{{ component.dependencies.length - 2 }}
                              </Badge>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </CardContent>
              </Card>

              <!-- Risk Scenarios -->
              <Card class="mt-6">
                <CardHeader>
                  <CardTitle>Risk Scenarios</CardTitle>
                  <CardDescription>
                    Identified risks and their potential impact
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="grid gap-4 md:grid-cols-2">
                    <div
                      v-for="risk in system.risks"
                      :key="risk.id"
                      class="rounded-lg border p-4 hover:shadow-md transition-shadow"
                    >
                      <div class="flex items-start justify-between mb-2">
                        <h4 class="font-medium">{{ risk.name }}</h4>
                        <Badge variant="outline">{{ risk.category_display }}</Badge>
                      </div>
                      <p class="text-sm text-muted-foreground mb-3">{{ risk.description }}</p>
                      <div class="flex gap-4 text-sm">
                        <div>
                          <span class="text-muted-foreground">Likelihood:</span>
                          <span :class="['ml-1 font-medium', risk.likelihood === 'high' ? 'text-red-600' : risk.likelihood === 'medium' ? 'text-amber-600' : 'text-green-600']">
                            {{ risk.likelihood_display }}
                          </span>
                        </div>
                        <div>
                          <span class="text-muted-foreground">Impact:</span>
                          <span :class="['ml-1 font-medium', risk.impact === 'high' ? 'text-red-600' : risk.impact === 'medium' ? 'text-amber-600' : 'text-green-600']">
                            {{ risk.impact }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <!-- Summary Stats -->
            <div class="space-y-6">
              <Card>
                <CardHeader class="pb-3">
                  <CardTitle class="text-base">Component Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <div class="space-y-4">
                    <div>
                      <div class="flex justify-between text-sm mb-1">
                        <span class="text-muted-foreground">Functional</span>
                        <span class="font-medium text-green-600">{{ system.components.filter(c => c.status === 'functional').length }}</span>
                      </div>
                      <Progress :model-value="(system.components.filter(c => c.status === 'functional').length / system.components.length) * 100" class="h-2 bg-green-100" />
                    </div>
                    <div>
                      <div class="flex justify-between text-sm mb-1">
                        <span class="text-muted-foreground">Degraded</span>
                        <span class="font-medium text-amber-600">{{ system.components.filter(c => c.status === 'degraded').length }}</span>
                      </div>
                      <Progress :model-value="(system.components.filter(c => c.status === 'degraded').length / system.components.length) * 100" class="h-2 bg-amber-100" />
                    </div>
                    <div>
                      <div class="flex justify-between text-sm mb-1">
                        <span class="text-muted-foreground">Non-functional</span>
                        <span class="font-medium text-red-600">{{ system.components.filter(c => c.status === 'non_functional').length }}</span>
                      </div>
                      <Progress :model-value="(system.components.filter(c => c.status === 'non_functional').length / system.components.length) * 100" class="h-2 bg-red-100" />
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader class="pb-3">
                  <CardTitle class="text-base">Categories</CardTitle>
                </CardHeader>
                <CardContent>
                  <div class="space-y-2">
                    <div v-for="category in ['infrastructure', 'human_resource', 'financial', 'information', 'governance']" :key="category" class="flex items-center justify-between">
                      <Badge :class="categoryColors[category]" variant="secondary" class="text-xs">
                        {{ category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) }}
                      </Badge>
                      <span class="text-sm font-medium">{{ system.components.filter(c => c.category === category).length }}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <!-- Chat Tab -->
        <TabsContent value="chat" class="mt-6">
          <Card class="h-[600px] flex flex-col">
            <CardHeader class="pb-3 border-b">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-goal/10">
                  <Bot class="h-5 w-5 text-goal" />
                </div>
                <div>
                  <CardTitle class="text-base">R4S Analysis Assistant</CardTitle>
                  <CardDescription class="text-xs">
                    Powered by Claude Opus 4.5 via Amazon Bedrock
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent class="flex-1 overflow-hidden flex flex-col p-0">
              <!-- Messages -->
              <div class="flex-1 overflow-y-auto p-4 space-y-4">
                <div
                  v-for="(message, index) in chatMessages"
                  :key="index"
                  :class="['flex', message.role === 'user' ? 'justify-end' : 'justify-start']"
                >
                  <div
                    :class="[
                      'max-w-[80%] rounded-lg px-4 py-3',
                      message.role === 'user'
                        ? 'bg-goal text-white'
                        : 'bg-muted'
                    ]"
                  >
                    <div class="text-sm whitespace-pre-wrap" v-html="message.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')"></div>
                  </div>
                </div>
                <div v-if="isTyping" class="flex justify-start">
                  <div class="bg-muted rounded-lg px-4 py-3">
                    <div class="flex items-center gap-2">
                      <div class="w-2 h-2 rounded-full bg-goal animate-bounce"></div>
                      <div class="w-2 h-2 rounded-full bg-goal animate-bounce" style="animation-delay: 0.1s"></div>
                      <div class="w-2 h-2 rounded-full bg-goal animate-bounce" style="animation-delay: 0.2s"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Input -->
              <div class="p-4 border-t bg-background">
                <form @submit.prevent="sendMessage" class="flex gap-2">
                  <Input
                    v-model="chatInput"
                    placeholder="Ask about vulnerabilities, actors, relationships..."
                    class="flex-1"
                  />
                  <Button type="submit" :disabled="!chatInput.trim() || isTyping">
                    <Send class="h-4 w-4" />
                  </Button>
                </form>
                <div class="mt-2 flex flex-wrap gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    class="text-xs"
                    @click="chatInput = 'What are the main vulnerabilities?'; sendMessage()"
                  >
                    Vulnerabilities
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    class="text-xs"
                    @click="chatInput = 'Tell me about the key actors'; sendMessage()"
                  >
                    Key Actors
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    class="text-xs"
                    @click="chatInput = 'What are your recommendations?'; sendMessage()"
                  >
                    Recommendations
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </template>
  </div>
</template>
