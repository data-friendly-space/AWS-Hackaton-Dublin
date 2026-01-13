<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

definePageMeta({
  layout: 'docs'
})

useHead({
  title: 'DSL Specification - Documentation - Resilio',
})

const actorTypes = [
  { value: 'service_user', desc: 'Directly demands, uses, and/or benefits from the goods/services/resources' },
  { value: 'service_provider', desc: 'Delivers core goods/services/resources directly to meet user needs' },
  { value: 'support', desc: 'Enables or enhances system performance through technical, financial, logistical assistance' },
  { value: 'regulatory', desc: 'Sets, enforces, and/or monitors rules, standards, and compliance' },
]

const qualityLevels = [
  { value: 'good', desc: 'Functions well for both actors, supports system performance' },
  { value: 'stressed', desc: "Inadequate or imbalanced; doesn't work ideally for both actors" },
  { value: 'bad', desc: "Fails to deliver benefits; doesn't support system objectives" },
  { value: 'absent', desc: 'Non-existent but should exist to support system objectives' },
]

const riskCategories = [
  { value: 'climate', desc: 'Weather, climate change related' },
  { value: 'health', desc: 'Disease, epidemic, pandemic' },
  { value: 'economic', desc: 'Market, financial, livelihood' },
  { value: 'conflict', desc: 'Violence, displacement, insecurity' },
  { value: 'natural', desc: 'Earthquake, flood, landslide' },
  { value: 'political', desc: 'Policy change, governance failure' },
]
</script>

<template>
  <div>
    <Badge class="mb-4">Language Specification</Badge>
    <h1 class="text-4xl font-bold text-goal-dark mb-4">.resilio DSL</h1>
    <p class="text-xl text-muted-foreground mb-8">
      A domain-specific language for defining social system maps, actors, relationships, and vulnerability assessments.
    </p>

    <!-- Overview -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Overview</h2>
      <div class="prose prose-slate max-w-none">
        <p>
          The Resilio DSL (<code class="bg-muted px-1 rounded">.resilio</code>) is a declarative language designed to represent
          the four core assessments of the Resilience for Social Systems (R4S) methodology:
        </p>
      </div>
      <div class="grid gap-4 md:grid-cols-2 mt-6">
        <Card>
          <CardContent class="pt-6">
            <h4 class="font-semibold text-goal-dark mb-2">Actor Assessment</h4>
            <p class="text-sm text-muted-foreground">Define system actors with their types, functions, needs, and concerns.</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <h4 class="font-semibold text-goal-dark mb-2">Relationship Assessment</h4>
            <p class="text-sm text-muted-foreground">Map interactions between actors with quality ratings and KPIs.</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <h4 class="font-semibold text-goal-dark mb-2">Component Assessment</h4>
            <p class="text-sm text-muted-foreground">Evaluate actor importance through production levels and replaceability.</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="pt-6">
            <h4 class="font-semibold text-goal-dark mb-2">Vulnerability Assessment</h4>
            <p class="text-sm text-muted-foreground">Assess actor vulnerabilities against defined risk scenarios.</p>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Basic Syntax -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Basic Syntax</h2>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle>Comments</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-slate-500"># This is a single-line comment</span>
<span class="text-slate-500">// This is also a single-line comment</span>

<span class="text-slate-500">/*
  This is a multi-line comment
  spanning multiple lines
*/</span></pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle>Strings</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-slate-500"># Single-line string</span>
<span class="text-green-400">"District Health Office"</span>

<span class="text-slate-500"># Multi-line string</span>
<span class="text-green-400">"""
This is a longer description
that spans multiple lines and preserves
line breaks and formatting.
"""</span></pre>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle>Blocks and Properties</CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground mb-4">
            Blocks group related declarations using curly braces. Properties are key-value pairs separated by colons.
          </p>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-amber-400">actor</span> <span class="text-yellow-300">DHO</span> {
    <span class="text-cyan-400">name</span>: <span class="text-green-400">"District Health Office"</span>
    <span class="text-cyan-400">type</span>: <span class="text-purple-400">service_provider</span>
}</pre>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- System Declaration -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">System Declaration</h2>
      <p class="text-muted-foreground mb-4">
        Every Resilio file begins with a <code class="bg-muted px-1 rounded">system</code> declaration that provides context for the assessment.
      </p>
      <Card>
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-amber-400">system</span> <span class="text-yellow-300">RMNCAH_Eastern</span> {
    <span class="text-cyan-400">name</span>: <span class="text-green-400">"RMNCAH Health System"</span>
    <span class="text-cyan-400">description</span>: <span class="text-green-400">"""
        Reproductive, Maternal, Newborn, Child, and Adolescent Health
        system serving the Eastern Region.
    """</span>
    <span class="text-cyan-400">region</span>: <span class="text-green-400">"Eastern Region"</span>
    <span class="text-cyan-400">country</span>: <span class="text-green-400">"Ethiopia"</span>
    <span class="text-cyan-400">sector</span>: <span class="text-purple-400">health</span>
    <span class="text-cyan-400">subsector</span>: <span class="text-green-400">"RMNCAH"</span>
    <span class="text-cyan-400">assessment_date</span>: <span class="text-green-400">"2026-01-15"</span>
    <span class="text-cyan-400">version</span>: <span class="text-green-400">"1.0"</span>
}</pre>
          </div>
          <div class="mt-4">
            <h4 class="font-medium mb-2">Sector Values</h4>
            <div class="flex flex-wrap gap-2">
              <Badge variant="secondary">health</Badge>
              <Badge variant="secondary">education</Badge>
              <Badge variant="secondary">market</Badge>
              <Badge variant="secondary">water</Badge>
              <Badge variant="secondary">protection</Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Actor Declaration -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Actor Declaration</h2>
      <p class="text-muted-foreground mb-4">
        Actors are the fundamental entities in the social system. Each actor declaration creates a unique entry in the Actor Assessment.
      </p>
      <Card class="mb-4">
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-amber-400">actor</span> <span class="text-yellow-300">DHO</span> {
    <span class="text-cyan-400">name</span>: <span class="text-green-400">"District Health Office"</span>
    <span class="text-cyan-400">type</span>: <span class="text-purple-400">service_provider</span>

    <span class="text-cyan-400">function</span>: <span class="text-green-400">"""
        Coordinates and oversees health service delivery across the district.
        Manages resource allocation, supervises health facilities.
    """</span>

    <span class="text-cyan-400">needs</span>: <span class="text-green-400">"""
        Adequate budget allocation, trained staff, medical supplies,
        reliable data reporting from facilities.
    """</span>

    <span class="text-cyan-400">worries</span>: <span class="text-green-400">"""
        Budget cuts, staff turnover, supply chain disruptions,
        disease outbreaks overwhelming capacity.
    """</span>
}</pre>
          </div>
        </CardContent>
      </Card>

      <h3 class="text-lg font-semibold mb-3">Actor Types</h3>
      <div class="grid gap-3 md:grid-cols-2">
        <div v-for="type in actorTypes" :key="type.value" class="rounded-lg border p-4">
          <code class="text-sm font-medium text-green-600">{{ type.value }}</code>
          <p class="text-sm text-muted-foreground mt-1">{{ type.desc }}</p>
        </div>
      </div>
    </div>

    <!-- Relationship Declaration -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Relationship Declaration</h2>
      <p class="text-muted-foreground mb-4">
        Relationships capture the flow of goods, services, and resources between actors. Two syntax options are available:
      </p>

      <Card class="mb-4">
        <CardHeader>
          <CardTitle>Arrow Syntax (Concise)</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-slate-500"># Output relationship (actor provides to another)</span>
<span class="text-yellow-300">DHO</span> <span class="text-pink-400">-></span> <span class="text-yellow-300">HealthCenter</span> {
    <span class="text-cyan-400">goods</span>: <span class="text-green-400">"Medical supplies, supervision"</span>
    <span class="text-cyan-400">quality</span>: <span class="text-purple-400">stressed</span>
    <span class="text-cyan-400">rationale</span>: <span class="text-green-400">"Delayed deliveries due to logistics"</span>
}

<span class="text-slate-500"># Input relationship (actor receives from another)</span>
<span class="text-yellow-300">HealthCenter</span> <span class="text-pink-400"><-</span> <span class="text-yellow-300">RegionalBureau</span> {
    <span class="text-cyan-400">goods</span>: <span class="text-green-400">"Budget allocation, policy directives"</span>
    <span class="text-cyan-400">quality</span>: <span class="text-purple-400">good</span>
}

<span class="text-slate-500"># Bidirectional relationship</span>
<span class="text-yellow-300">HealthCenter</span> <span class="text-pink-400"><-></span> <span class="text-yellow-300">Community</span> {
    <span class="text-cyan-400">goods</span>: <span class="text-green-400">"Health services | Feedback, utilization"</span>
    <span class="text-cyan-400">quality</span>: <span class="text-purple-400">good</span>
}</pre>
          </div>
        </CardContent>
      </Card>

      <h3 class="text-lg font-semibold mb-3">Quality Levels</h3>
      <div class="grid gap-3 md:grid-cols-2">
        <div v-for="quality in qualityLevels" :key="quality.value" class="rounded-lg border p-4">
          <code class="text-sm font-medium text-green-600">{{ quality.value }}</code>
          <p class="text-sm text-muted-foreground mt-1">{{ quality.desc }}</p>
        </div>
      </div>
    </div>

    <!-- Component Assessment -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Component Assessment</h2>
      <p class="text-muted-foreground mb-4">
        Component assessments measure each actor's contribution to the system and how easily they could be replaced.
        The relevance score is calculated as: <code class="bg-muted px-1 rounded">production x replaceability</code>
      </p>
      <Card>
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-amber-400">component</span> <span class="text-yellow-300">DHO</span> {
    <span class="text-cyan-400">goods</span>: <span class="text-green-400">"Coordination, supervision, supply distribution"</span>

    <span class="text-cyan-400">production</span>: <span class="text-orange-400">4</span>  <span class="text-slate-500"># High contribution (61-80%)</span>
    <span class="text-cyan-400">replaceability</span>: <span class="text-orange-400">5</span>  <span class="text-slate-500"># Not replaceable</span>

    <span class="text-cyan-400">rationale</span>: <span class="text-green-400">"""
        The DHO plays a major role in coordinating all health services.
        As the sole government coordination body, there is no viable substitute.
    """</span>
}

<span class="text-slate-500"># Relevance score: production x replaceability = 20</span></pre>
          </div>
          <div class="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <h4 class="font-medium mb-2">Production Scale (1-5)</h4>
              <div class="text-sm text-muted-foreground space-y-1">
                <div><strong>1:</strong> Minimal (1-20%)</div>
                <div><strong>2:</strong> Low (21-40%)</div>
                <div><strong>3:</strong> Moderate (41-60%)</div>
                <div><strong>4:</strong> High (61-80%)</div>
                <div><strong>5:</strong> Very High (81-100%)</div>
              </div>
            </div>
            <div>
              <h4 class="font-medium mb-2">Replaceability Scale (1-5)</h4>
              <div class="text-sm text-muted-foreground space-y-1">
                <div><strong>1:</strong> Highly replaceable</div>
                <div><strong>2:</strong> Easily replaceable</div>
                <div><strong>3:</strong> Moderately replaceable</div>
                <div><strong>4:</strong> Hard to replace</div>
                <div><strong>5:</strong> Not replaceable</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Vulnerability Assessment -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Vulnerability Assessment</h2>
      <p class="text-muted-foreground mb-4">
        Vulnerability assessments evaluate each actor against defined risk scenarios using sensitivity, exposure, and capacity metrics.
        Score is calculated as: <code class="bg-muted px-1 rounded">(sensitivity + exposure) / capacity</code>
      </p>
      <Card>
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-amber-400">vulnerability</span> <span class="text-yellow-300">DHO</span> <span class="text-pink-400">@</span> <span class="text-yellow-300">drought</span> {
    <span class="text-cyan-400">sensitivity</span>: <span class="text-orange-400">3</span>    <span class="text-slate-500"># Moderate impact</span>
    <span class="text-cyan-400">exposure</span>: <span class="text-orange-400">4</span>       <span class="text-slate-500"># High exposure</span>
    <span class="text-cyan-400">capacity</span>: <span class="text-orange-400">3</span>       <span class="text-slate-500"># Moderate coping ability</span>

    <span class="text-cyan-400">rationale</span>: <span class="text-green-400">"""
        Drought increases demand for health services while simultaneously
        straining resources. The DHO has some emergency protocols but
        limited surge capacity.
    """</span>
}

<span class="text-slate-500"># Vulnerability score: (3+4)/3 = 2.3 (Low)</span></pre>
          </div>
          <div class="mt-4">
            <h4 class="font-medium mb-2">Vulnerability Levels</h4>
            <div class="grid gap-2 md:grid-cols-4">
              <div class="text-sm"><Badge class="bg-green-100 text-green-700">0-1.0: Minimal</Badge></div>
              <div class="text-sm"><Badge class="bg-lime-100 text-lime-700">1.1-8.33: Low</Badge></div>
              <div class="text-sm"><Badge class="bg-amber-100 text-amber-700">8.34-16.66: Medium</Badge></div>
              <div class="text-sm"><Badge class="bg-red-100 text-red-700">16.67-25: High</Badge></div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Risk Scenarios -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Risk Scenario Declaration</h2>
      <p class="text-muted-foreground mb-4">
        Risk scenarios must be declared before they can be referenced in vulnerability assessments.
      </p>
      <Card class="mb-4">
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
            <pre><span class="text-amber-400">risk</span> <span class="text-yellow-300">drought</span> {
    <span class="text-cyan-400">name</span>: <span class="text-green-400">"Severe Drought"</span>
    <span class="text-cyan-400">description</span>: <span class="text-green-400">"""
        Extended period of below-normal rainfall leading to water scarcity,
        crop failure, and increased food insecurity.
    """</span>
    <span class="text-cyan-400">category</span>: <span class="text-purple-400">climate</span>
    <span class="text-cyan-400">likelihood</span>: <span class="text-purple-400">likely</span>
    <span class="text-cyan-400">historical</span>: <span class="text-green-400">"2015, 2017, 2022"</span>
}</pre>
          </div>
        </CardContent>
      </Card>

      <h3 class="text-lg font-semibold mb-3">Risk Categories</h3>
      <div class="grid gap-3 md:grid-cols-3">
        <div v-for="cat in riskCategories" :key="cat.value" class="rounded-lg border p-4">
          <code class="text-sm font-medium text-green-600">{{ cat.value }}</code>
          <p class="text-sm text-muted-foreground mt-1">{{ cat.desc }}</p>
        </div>
      </div>

      <div class="mt-4">
        <h3 class="text-lg font-semibold mb-3">Likelihood Levels</h3>
        <div class="flex flex-wrap gap-2">
          <Badge variant="outline">rare (&lt;10%)</Badge>
          <Badge variant="outline">unlikely (10-30%)</Badge>
          <Badge variant="outline">possible (30-60%)</Badge>
          <Badge variant="outline">likely (60-90%)</Badge>
          <Badge variant="outline">almost_certain (&gt;90%)</Badge>
        </div>
      </div>
    </div>

    <!-- Grammar Reference -->
    <div>
      <h2 class="text-2xl font-bold text-goal-dark mb-4">Grammar Reference</h2>
      <Card>
        <CardContent class="pt-6">
          <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-xs overflow-x-auto">
            <pre>document        ::= system_decl (risk_decl | actor_decl | relationship_decl | component_decl | vulnerability_decl)*

system_decl     ::= "system" identifier "{" system_props "}"
risk_decl       ::= "risk" identifier "{" risk_props "}"
actor_decl      ::= "actor" identifier "{" actor_props "}"

relationship_decl ::= relationship_block | relationship_arrow
relationship_block ::= "relationship" identifier "{" relationship_props "}"
relationship_arrow ::= identifier arrow_op identifier "{" relationship_props "}"
arrow_op        ::= "->" | "<-" | "<->"

component_decl  ::= "component" identifier "{" component_props "}"
vulnerability_decl ::= "vulnerability" identifier "@" identifier "{" vulnerability_props "}"

property        ::= identifier ":" value
value           ::= string | number | enum_value | identifier | list
list            ::= "[" (value ("," value)*)? "]"

actor_type      ::= "service_user" | "service_provider" | "support" | "regulatory"
rel_quality     ::= "good" | "stressed" | "bad" | "absent"
risk_category   ::= "climate" | "health" | "economic" | "conflict" | "natural" | "political"
likelihood      ::= "rare" | "unlikely" | "possible" | "likely" | "almost_certain"
sector          ::= "health" | "education" | "market" | "water" | "protection"</pre>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
