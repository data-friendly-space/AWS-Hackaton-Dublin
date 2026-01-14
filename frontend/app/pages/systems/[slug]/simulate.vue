<script setup lang="ts">
import type { SimulationScenario, SimulationEvent } from '~/types/simulation'
import { EVENT_TYPE_INFO, PRIORITY_INFO } from '~/types/simulation'

const route = useRoute()
const slug = computed(() => route.params.slug as string)

// Use mock data (same as main system page)
const { getSystemBySlug } = useMockSystems()
const system = getSystemBySlug(slug.value)

// Get actors and relationships from mock data
const actors = computed(() => system?.actors || [])
const relationships = computed(() => system?.relationships || [])

// Simulation state
const simulation = useSimulation(slug)
const {
  state: simState,
  sortedEvents,
  activeRemediations,
  loadScenario,
  clearScenario,
  play,
  pause,
  stop,
  seekToDay,
  setSpeed,
  getActorQuality,
  getRelationshipQuality,
} = simulation

// UI State
const showChatPanel = ref(false)
const selectedScenarioIndex = ref<number | null>(null)

// Canvas for network graph
const canvasRef = ref<HTMLCanvasElement | null>(null)
const canvasContainerRef = ref<HTMLDivElement | null>(null)

// View state
const scale = ref(1)
const offsetX = ref(0)
const offsetY = ref(0)

// Drag state
const dragging = ref(false)
const dragNode = ref<any>(null)
const dragStartX = ref(0)
const dragStartY = ref(0)
const hoveredNode = ref<any>(null)
const selectedNode = ref<any>(null)

// Nodes and edges for visualization
const visNodes = ref<any[]>([])
const visEdges = ref<any[]>([])

// Animation state
const animationTime = ref(0)
const animationFrameId = ref<number | null>(null)

// Mock scenarios for demonstration
const mockScenarios: SimulationScenario[] = [
  {
    scenario: {
      name: 'Drought Impact Scenario',
      description: 'Simulates a 3-month drought affecting health services in Eastern Ethiopia',
      duration: 90,
    },
    events: [
      {
        day: 0,
        type: 'disaster_onset',
        name: 'Drought Declared',
        description: 'Regional government declares drought emergency affecting pastoral communities',
        impacts: [],
        remediations: [],
      },
      {
        day: 14,
        type: 'resource_shortage',
        name: 'Water Scarcity at Health Centers',
        description: 'Health centers report critical water shortages affecting sanitation and patient care',
        impacts: [
          { actor: 'a3', attribute: 'quality', from: 'good', to: 'stressed' },
          { actor: 'a4', attribute: 'quality', from: 'good', to: 'stressed' },
        ],
        remediations: [
          { priority: 'high', action: 'Deploy emergency water tanks to affected facilities', actor: 'NGO Partners' },
          { priority: 'medium', action: 'Implement water rationing protocols', actor: 'Health Centers' },
        ],
      },
      {
        day: 30,
        type: 'demand_surge',
        name: 'Malnutrition Cases Increase',
        description: 'Acute malnutrition cases among children under 5 increase by 40%',
        impacts: [
          { actor: 'a2', attribute: 'quality', from: 'good', to: 'stressed' },
          { relationship: 'a3 -> a2', attribute: 'quality', from: 'good', to: 'stressed' },
        ],
        remediations: [
          { priority: 'critical', action: 'Activate emergency nutrition program', actor: 'Regional Health Bureau' },
          { priority: 'high', action: 'Deploy mobile health teams to affected areas', actor: 'Health Extension Workers' },
        ],
      },
      {
        day: 45,
        type: 'capacity_reduction',
        name: 'Staff Shortages',
        description: 'Health workers face personal hardship, reducing available workforce by 25%',
        impacts: [
          { actor: 'a5', attribute: 'quality', from: 'good', to: 'bad' },
          { actor: 'a6', attribute: 'quality', from: 'good', to: 'stressed' },
        ],
        remediations: [
          { priority: 'high', action: 'Provide hardship allowances to retain staff', actor: 'Regional Health Bureau' },
          { priority: 'medium', action: 'Request volunteer health workers from partner organizations', actor: 'NGO Partners' },
        ],
      },
      {
        day: 60,
        type: 'intervention',
        name: 'Emergency Response Activated',
        description: 'Coordinated emergency response begins with additional resources',
        impacts: [
          { actor: 'a3', attribute: 'quality', from: 'stressed', to: 'good' },
          { actor: 'a8', attribute: 'quality', from: 'good', to: 'stressed' },
        ],
        remediations: [],
      },
      {
        day: 80,
        type: 'recovery',
        name: 'Services Stabilizing',
        description: 'Health services beginning to recover as drought conditions ease',
        impacts: [
          { actor: 'a4', attribute: 'quality', from: 'stressed', to: 'good' },
          { actor: 'a5', attribute: 'quality', from: 'bad', to: 'stressed' },
        ],
        remediations: [
          { priority: 'medium', action: 'Begin post-emergency assessment', actor: 'Regional Health Bureau' },
        ],
      },
    ],
  },
  {
    scenario: {
      name: 'Disease Outbreak Response',
      description: 'Cholera outbreak affecting communities served by the health system',
      duration: 60,
    },
    events: [
      {
        day: 0,
        type: 'disaster_onset',
        name: 'Cholera Cases Detected',
        description: 'First cholera cases confirmed in multiple woredas',
        impacts: [
          { actor: 'a1', attribute: 'quality', from: 'good', to: 'stressed' },
          { actor: 'a2', attribute: 'quality', from: 'good', to: 'stressed' },
        ],
        remediations: [
          { priority: 'critical', action: 'Activate disease outbreak response protocol', actor: 'Regional Health Bureau' },
        ],
      },
      {
        day: 7,
        type: 'demand_surge',
        name: 'Case Surge',
        description: 'Daily new cases exceed health center capacity',
        impacts: [
          { actor: 'a3', attribute: 'quality', from: 'good', to: 'bad' },
          { actor: 'a4', attribute: 'quality', from: 'good', to: 'bad' },
        ],
        remediations: [
          { priority: 'critical', action: 'Establish cholera treatment centers', actor: 'Health Centers' },
          { priority: 'high', action: 'Deploy oral rehydration supplies', actor: 'NGO Partners' },
        ],
      },
      {
        day: 21,
        type: 'intervention',
        name: 'Mass Vaccination Campaign',
        description: 'Oral cholera vaccine campaign launched',
        impacts: [
          { actor: 'a3', attribute: 'quality', from: 'bad', to: 'stressed' },
        ],
        remediations: [],
      },
      {
        day: 45,
        type: 'recovery',
        name: 'Outbreak Contained',
        description: 'New cases declining, outbreak under control',
        impacts: [
          { actor: 'a3', attribute: 'quality', from: 'stressed', to: 'good' },
          { actor: 'a4', attribute: 'quality', from: 'bad', to: 'good' },
          { actor: 'a1', attribute: 'quality', from: 'stressed', to: 'good' },
        ],
        remediations: [
          { priority: 'medium', action: 'Conduct lessons learned review', actor: 'Regional Health Bureau' },
        ],
      },
    ],
  },
  {
    scenario: {
      name: 'Funding Reduction Impact',
      description: 'Impact of 30% funding cut to health programs',
      duration: 120,
    },
    events: [
      {
        day: 0,
        type: 'disaster_onset',
        name: 'Budget Cuts Announced',
        description: 'Government announces 30% reduction in health sector funding',
        impacts: [],
        remediations: [
          { priority: 'high', action: 'Develop contingency budget plan', actor: 'Regional Health Bureau' },
        ],
      },
      {
        day: 30,
        type: 'resource_shortage',
        name: 'Supply Chain Disruption',
        description: 'Essential medicine supplies reduced due to procurement cuts',
        impacts: [
          { actor: 'a7', attribute: 'quality', from: 'good', to: 'stressed' },
          { relationship: 'a7 -> a3', attribute: 'quality', from: 'good', to: 'stressed' },
        ],
        remediations: [
          { priority: 'high', action: 'Prioritize essential medicines list', actor: 'Regional Health Bureau' },
          { priority: 'medium', action: 'Seek emergency donor funding', actor: 'NGO Partners' },
        ],
      },
      {
        day: 60,
        type: 'capacity_reduction',
        name: 'Staff Reductions',
        description: 'Contract health workers not renewed, reducing workforce',
        impacts: [
          { actor: 'a5', attribute: 'quality', from: 'good', to: 'stressed' },
          { actor: 'a6', attribute: 'quality', from: 'good', to: 'stressed' },
        ],
        remediations: [
          { priority: 'critical', action: 'Advocate for restored funding', actor: 'Regional Health Bureau' },
        ],
      },
      {
        day: 90,
        type: 'infrastructure_damage',
        name: 'Service Reduction',
        description: 'Health posts reduce operating hours due to budget constraints',
        impacts: [
          { actor: 'a4', attribute: 'quality', from: 'good', to: 'bad' },
          { relationship: 'a4 -> a1', attribute: 'quality', from: 'good', to: 'bad' },
        ],
        remediations: [
          { priority: 'high', action: 'Implement community health volunteer program', actor: 'Health Extension Workers' },
        ],
      },
    ],
  },
]

// Actor type colors (same as main page)
const visColors: Record<string, string> = {
  service_user: '#8B5CF6',
  service_provider: '#006e33',
  support: '#F59E0B',
  regulatory: '#EF4444',
  good: '#22C55E',
  stressed: '#F59E0B',
  bad: '#EF4444',
  absent: '#9CA3AF'
}

// Load selected scenario
function selectScenario(index: number) {
  selectedScenarioIndex.value = index
  loadScenario(mockScenarios[index])
}

// Handle scenario from chat
function handleScenarioGenerated(scenario: SimulationScenario) {
  loadScenario(scenario)
  showChatPanel.value = false
  selectedScenarioIndex.value = null
}

// Initialize visualization
function initVisualization() {
  if (!canvasRef.value || !canvasContainerRef.value || !system) return

  const canvas = canvasRef.value
  const container = canvasContainerRef.value

  const containerWidth = container.clientWidth || 800
  const containerHeight = container.clientHeight || 500

  canvas.width = containerWidth
  canvas.height = containerHeight

  const centerX = canvas.width / 2
  const centerY = canvas.height / 2
  const radius = Math.min(centerX, centerY) * 0.6

  visNodes.value = actors.value.map((actor: any, i: number) => {
    const angle = (i / actors.value.length) * Math.PI * 2 - Math.PI / 2
    return {
      id: actor.id,
      x: centerX + Math.cos(angle) * radius,
      y: centerY + Math.sin(angle) * radius,
      radius: 35,
      data: actor,
      color: visColors[actor.actor_type] || '#6B7280'
    }
  })

  visEdges.value = relationships.value.map((rel: any) => {
    const fromNode = visNodes.value.find(n => n.data.name === rel.from_actor_name)
    const toNode = visNodes.value.find(n => n.data.name === rel.to_actor_name)
    return {
      from: fromNode,
      to: toNode,
      data: rel
    }
  }).filter((e: any) => e.from && e.to)

  runForceLayout()
  renderCanvas()
}

function runForceLayout() {
  const iterations = 80
  const k = 120
  const gravity = 0.1
  const canvas = canvasRef.value
  if (!canvas) return

  const centerX = canvas.width / 2 / scale.value
  const centerY = canvas.height / 2 / scale.value

  for (let iter = 0; iter < iterations; iter++) {
    // Repulsion
    for (let i = 0; i < visNodes.value.length; i++) {
      for (let j = i + 1; j < visNodes.value.length; j++) {
        const dx = visNodes.value[j].x - visNodes.value[i].x
        const dy = visNodes.value[j].y - visNodes.value[i].y
        const dist = Math.max(1, Math.sqrt(dx * dx + dy * dy))
        const force = (k * k) / dist
        const fx = (dx / dist) * force
        const fy = (dy / dist) * force
        visNodes.value[i].x -= fx * 0.1
        visNodes.value[i].y -= fy * 0.1
        visNodes.value[j].x += fx * 0.1
        visNodes.value[j].y += fy * 0.1
      }
    }

    // Attraction along edges
    for (const edge of visEdges.value) {
      if (!edge.from || !edge.to) continue
      const dx = edge.to.x - edge.from.x
      const dy = edge.to.y - edge.from.y
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist === 0) continue
      const force = (dist - k) * 0.1
      const fx = (dx / dist) * force
      const fy = (dy / dist) * force
      edge.from.x += fx * 0.1
      edge.from.y += fy * 0.1
      edge.to.x -= fx * 0.1
      edge.to.y -= fy * 0.1
    }

    // Gravity
    for (const node of visNodes.value) {
      node.x += (centerX - node.x) * gravity * 0.1
      node.y += (centerY - node.y) * gravity * 0.1
    }
  }

  centerView()
}

function centerView() {
  if (visNodes.value.length === 0 || !canvasRef.value) return

  let minX = Infinity, maxX = -Infinity
  let minY = Infinity, maxY = -Infinity

  for (const node of visNodes.value) {
    minX = Math.min(minX, node.x - node.radius)
    maxX = Math.max(maxX, node.x + node.radius)
    minY = Math.min(minY, node.y - node.radius)
    maxY = Math.max(maxY, node.y + node.radius)
  }

  const width = maxX - minX
  const height = maxY - minY
  const graphCenterX = (minX + maxX) / 2
  const graphCenterY = (minY + maxY) / 2

  const scaleX = (canvasRef.value.width - 100) / width
  const scaleY = (canvasRef.value.height - 100) / height
  scale.value = Math.min(1.5, Math.min(scaleX, scaleY))

  offsetX.value = canvasRef.value.width / 2 - graphCenterX * scale.value
  offsetY.value = canvasRef.value.height / 2 - graphCenterY * scale.value
}

function renderCanvas() {
  if (!canvasRef.value) return
  const ctx = canvasRef.value.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)
  ctx.save()
  ctx.translate(offsetX.value, offsetY.value)
  ctx.scale(scale.value, scale.value)

  // Draw edges
  for (const edge of visEdges.value) {
    drawEdge(ctx, edge, animationTime.value)
  }

  // Draw nodes
  for (const node of visNodes.value) {
    drawNode(ctx, node)
  }

  ctx.restore()
}

function drawNode(ctx: CanvasRenderingContext2D, node: any) {
  const { x, y, radius, data } = node
  const isHovered = node === hoveredNode.value
  const isSelected = node === selectedNode.value

  // Get effective quality from simulation (if active) or use base color
  let effectiveQuality: string | null = null
  if (simState.scenario && typeof getActorQuality === 'function') {
    effectiveQuality = getActorQuality(node.id, 'good')
  }

  // Determine node color
  let color = node.color
  if (effectiveQuality && effectiveQuality !== 'good') {
    color = visColors[effectiveQuality] || node.color
  }

  // Node background with glow effect for affected nodes
  if (effectiveQuality && effectiveQuality !== 'good') {
    // Add glow for affected nodes
    ctx.shadowColor = color
    ctx.shadowBlur = 15
  }

  ctx.beginPath()
  ctx.arc(x, y, radius, 0, Math.PI * 2)
  ctx.fillStyle = isHovered || isSelected ? lightenColor(color, 20) : color
  ctx.fill()

  ctx.shadowColor = 'transparent'
  ctx.shadowBlur = 0

  // Selection ring
  if (isSelected) {
    ctx.strokeStyle = '#1A1F2E'
    ctx.lineWidth = 3
    ctx.stroke()
  }

  // Node letter
  ctx.fillStyle = 'white'
  ctx.font = `bold ${radius * 0.5}px Inter, sans-serif`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText(data.name?.charAt(0) || '?', x, y)

  // Label
  ctx.fillStyle = '#1A1F2E'
  ctx.font = '11px Inter, sans-serif'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'top'
  const label = data.name || node.id
  const truncatedLabel = label.length > 15 ? label.substring(0, 15) + '...' : label
  ctx.fillText(truncatedLabel, x, y + radius + 8)
}

function drawEdge(ctx: CanvasRenderingContext2D, edge: any, time: number = 0) {
  const { from, to, data } = edge
  if (!from || !to) return

  const dx = to.x - from.x
  const dy = to.y - from.y
  const dist = Math.sqrt(dx * dx + dy * dy)
  if (dist === 0) return

  const nx = dx / dist
  const ny = dy / dist

  const startX = from.x + nx * from.radius
  const startY = from.y + ny * from.radius
  const endX = to.x - nx * to.radius
  const endY = to.y - ny * to.radius

  // Get effective quality from simulation (if active) or use base quality
  let quality = data.quality || 'good'
  if (simState.scenario && typeof getRelationshipQuality === 'function') {
    quality = getRelationshipQuality(from.id, to.id, quality)
  }

  let baseColor = visColors[quality] || '#9CA3AF'
  let lineWidth = quality === 'absent' ? 2 : quality === 'good' ? 4 : 5

  // Pulsing animation for stressed and bad relationships
  if (quality === 'stressed' || quality === 'bad') {
    const pulseSpeed = quality === 'bad' ? 4 : 2
    const pulse = Math.sin(time * pulseSpeed / 1000 * Math.PI) * 0.3 + 0.7
    ctx.globalAlpha = pulse
    lineWidth = lineWidth + Math.sin(time * pulseSpeed / 1000 * Math.PI) * 1.5
  } else {
    ctx.globalAlpha = 1
  }

  ctx.strokeStyle = baseColor
  ctx.lineWidth = lineWidth

  if (quality === 'absent') {
    ctx.setLineDash([8, 8])
  } else if (quality === 'stressed') {
    ctx.setLineDash([12, 6])
  } else {
    ctx.setLineDash([])
  }

  ctx.beginPath()
  ctx.moveTo(startX, startY)
  ctx.lineTo(endX, endY)
  ctx.stroke()

  // Arrow
  const arrowSize = 12
  const angle = Math.atan2(endY - startY, endX - startX)
  ctx.beginPath()
  ctx.moveTo(endX, endY)
  ctx.lineTo(endX - arrowSize * Math.cos(angle - Math.PI / 6), endY - arrowSize * Math.sin(angle - Math.PI / 6))
  ctx.lineTo(endX - arrowSize * Math.cos(angle + Math.PI / 6), endY - arrowSize * Math.sin(angle + Math.PI / 6))
  ctx.closePath()
  ctx.fillStyle = ctx.strokeStyle
  ctx.fill()
  ctx.setLineDash([])
  ctx.globalAlpha = 1
}

function lightenColor(hex: string, percent: number): string {
  const num = parseInt(hex.replace('#', ''), 16)
  const amt = Math.round(2.55 * percent)
  const R = Math.min(255, (num >> 16) + amt)
  const G = Math.min(255, ((num >> 8) & 0x00FF) + amt)
  const B = Math.min(255, (num & 0x0000FF) + amt)
  return '#' + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1)
}

function screenToWorld(x: number, y: number) {
  return {
    x: (x - offsetX.value) / scale.value,
    y: (y - offsetY.value) / scale.value
  }
}

// Mouse handlers for pan/drag
function onCanvasMouseDown(e: MouseEvent) {
  const rect = canvasRef.value?.getBoundingClientRect()
  if (!rect) return
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top
  const world = screenToWorld(mouseX, mouseY)

  for (const node of visNodes.value) {
    const dx = world.x - node.x
    const dy = world.y - node.y
    if (Math.sqrt(dx * dx + dy * dy) < node.radius) {
      dragNode.value = node
      selectedNode.value = node
      renderCanvas()
      return
    }
  }

  dragging.value = true
  dragStartX.value = mouseX - offsetX.value
  dragStartY.value = mouseY - offsetY.value
}

function onCanvasMouseMove(e: MouseEvent) {
  const rect = canvasRef.value?.getBoundingClientRect()
  if (!rect) return
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top

  if (dragNode.value) {
    const world = screenToWorld(mouseX, mouseY)
    dragNode.value.x = world.x
    dragNode.value.y = world.y
    renderCanvas()
    return
  }

  if (dragging.value) {
    offsetX.value = mouseX - dragStartX.value
    offsetY.value = mouseY - dragStartY.value
    renderCanvas()
    return
  }

  // Hover detection
  const world = screenToWorld(mouseX, mouseY)
  let found = null
  for (const node of visNodes.value) {
    const dx = world.x - node.x
    const dy = world.y - node.y
    if (Math.sqrt(dx * dx + dy * dy) < node.radius) {
      found = node
      break
    }
  }
  if (found !== hoveredNode.value) {
    hoveredNode.value = found
    renderCanvas()
  }
}

function onCanvasMouseUp() {
  dragNode.value = null
  dragging.value = false
}

function onCanvasWheel(e: WheelEvent) {
  e.preventDefault()
  const rect = canvasRef.value?.getBoundingClientRect()
  if (!rect) return

  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top

  const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9
  const newScale = Math.max(0.3, Math.min(3, scale.value * zoomFactor))

  offsetX.value = mouseX - (mouseX - offsetX.value) * (newScale / scale.value)
  offsetY.value = mouseY - (mouseY - offsetY.value) * (newScale / scale.value)
  scale.value = newScale

  renderCanvas()
}

// Animation loop
function startAnimation() {
  if (animationFrameId.value) return

  const animate = () => {
    animationTime.value = Date.now()
    renderCanvas()
    animationFrameId.value = requestAnimationFrame(animate)
  }
  animate()
}

function stopAnimation() {
  if (animationFrameId.value) {
    cancelAnimationFrame(animationFrameId.value)
    animationFrameId.value = null
  }
}

// Watch simulation state changes
watch(() => simState.currentDay, () => {
  renderCanvas()
})

watch(() => simState.isPlaying, (playing) => {
  if (playing) {
    startAnimation()
  }
})

// Initialize on mount
onMounted(() => {
  nextTick(() => {
    initVisualization()
    startAnimation()
  })
})

onUnmounted(() => {
  stopAnimation()
})

// Handle window resize
onMounted(() => {
  const resizeHandler = () => {
    if (canvasRef.value && canvasContainerRef.value) {
      canvasRef.value.width = canvasContainerRef.value.clientWidth
      canvasRef.value.height = canvasContainerRef.value.clientHeight
      renderCanvas()
    }
  }
  window.addEventListener('resize', resizeHandler)
  onUnmounted(() => window.removeEventListener('resize', resizeHandler))
})
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-white border-b-2 border-gray-300 shadow-sm">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <NuxtLink
              :to="`/systems/${slug}`"
              class="text-gray-500 hover:text-gray-700"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </NuxtLink>
            <div>
              <h1 class="text-xl font-bold text-gray-900">Risk Simulator</h1>
              <p class="text-sm text-gray-500">{{ system?.name }}</p>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <!-- Create new -->
            <button
              @click="showChatPanel = true"
              class="px-4 py-2 bg-green-700 text-white rounded-lg hover:bg-green-800 flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              Ask AI
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <div class="container mx-auto px-4 py-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left column: Graph + Timeline -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Network Graph -->
          <div class="bg-white rounded-xl border-2 border-gray-300 shadow-md p-4">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-bold text-gray-900">Network Impact Visualization</h2>
              <div v-if="simState.scenario" class="flex items-center gap-2 text-sm">
                <span class="px-2 py-1 bg-green-100 text-green-700 rounded">
                  {{ simState.scenario.scenario.name }}
                </span>
              </div>
            </div>
            <div
              ref="canvasContainerRef"
              class="relative w-full h-[450px] bg-gray-100 rounded-lg overflow-hidden border border-gray-200"
            >
              <canvas
                ref="canvasRef"
                class="w-full h-full cursor-grab active:cursor-grabbing"
                @mousedown="onCanvasMouseDown"
                @mousemove="onCanvasMouseMove"
                @mouseup="onCanvasMouseUp"
                @mouseleave="onCanvasMouseUp"
                @wheel="onCanvasWheel"
              />

              <!-- Overlay when no scenario -->
              <div
                v-if="!simState.scenario"
                class="absolute inset-0 flex items-center justify-center bg-gray-200/70 pointer-events-none"
              >
                <div class="text-center bg-white/90 rounded-lg px-6 py-4 shadow">
                  <div class="text-4xl mb-2">📊</div>
                  <p class="text-gray-600 font-medium">Select a scenario to see impact visualization</p>
                </div>
              </div>
            </div>

            <!-- Legend -->
            <div class="flex flex-wrap items-center gap-x-6 gap-y-2 mt-4 text-sm text-gray-700 font-medium">
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full bg-green-500 border border-gray-400" />
                <span>Good</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full bg-yellow-500 border border-gray-400" />
                <span>Stressed</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full bg-red-500 border border-gray-400" />
                <span>Bad</span>
              </div>
              <div class="border-l-2 border-gray-300 pl-6 flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full bg-purple-500 border border-gray-400" />
                <span>Service User</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full bg-green-700 border border-gray-400" />
                <span>Provider</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full bg-yellow-500 border border-gray-400" />
                <span>Support</span>
              </div>
            </div>
          </div>

          <!-- Timeline -->
          <SimulationTimeline
            :scenario="simState.scenario"
            :current-day="simState.currentDay"
            :is-playing="simState.isPlaying"
            :playback-speed="simState.playbackSpeed"
            @play="play"
            @pause="pause"
            @stop="stop"
            @seek="seekToDay"
            @speed="setSpeed"
          />
        </div>

        <!-- Right column: Scenario selector + Event details -->
        <div class="space-y-6">
          <!-- Scenario Selector -->
          <div class="bg-white rounded-xl border-2 border-gray-300 shadow-md p-4">
            <h3 class="font-bold text-gray-900 mb-3">Select Scenario</h3>

            <div class="space-y-2">
              <button
                v-for="(scenario, index) in mockScenarios"
                :key="index"
                @click="selectScenario(index)"
                :class="[
                  'w-full text-left p-3 rounded-lg border-2 transition-colors',
                  selectedScenarioIndex === index
                    ? 'border-green-700 bg-green-50 shadow-sm'
                    : 'border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-white',
                ]"
              >
                <div class="font-medium text-gray-900">{{ scenario.scenario.name }}</div>
                <div class="text-xs text-gray-500 mt-1">
                  {{ scenario.scenario.duration }} days · {{ scenario.events.length }} events
                </div>
                <div class="text-xs text-gray-400 mt-1 line-clamp-2">
                  {{ scenario.scenario.description }}
                </div>
              </button>
            </div>

            <button
              v-if="simState.scenario"
              @click="clearScenario(); selectedScenarioIndex = null"
              class="w-full mt-3 px-3 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              Clear Scenario
            </button>
          </div>

          <!-- Current Event Details -->
          <div v-if="simState.activeEvent" class="bg-white rounded-xl border-2 border-gray-300 shadow-md p-4">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-2xl">{{ EVENT_TYPE_INFO[simState.activeEvent.type]?.icon }}</span>
              <div>
                <h3 class="font-semibold text-gray-900">{{ simState.activeEvent.name }}</h3>
                <p class="text-xs text-gray-500">Day {{ simState.activeEvent.day }}</p>
              </div>
            </div>

            <p class="text-sm text-gray-600 mb-4">{{ simState.activeEvent.description }}</p>

            <!-- Impacts -->
            <div v-if="simState.activeEvent.impacts.length > 0" class="mb-4">
              <h4 class="text-sm font-medium text-gray-700 mb-2">Impacts</h4>
              <ul class="space-y-1">
                <li
                  v-for="(impact, i) in simState.activeEvent.impacts"
                  :key="i"
                  class="text-sm text-gray-600 flex items-center gap-2"
                >
                  <span class="w-1.5 h-1.5 rounded-full bg-red-500" />
                  <span v-if="impact.actor">{{ impact.actor }}</span>
                  <span v-else>{{ impact.relationship }}</span>
                  <span class="text-gray-400">→</span>
                  <span
                    class="px-1.5 py-0.5 rounded text-xs font-medium"
                    :style="{ backgroundColor: visColors[impact.to as string] + '20', color: visColors[impact.to as string] }"
                  >
                    {{ impact.to }}
                  </span>
                </li>
              </ul>
            </div>

            <!-- Remediations -->
            <div v-if="simState.activeEvent.remediations.length > 0">
              <h4 class="text-sm font-medium text-gray-700 mb-2">Suggested Actions</h4>
              <ul class="space-y-2">
                <li
                  v-for="(rem, i) in simState.activeEvent.remediations"
                  :key="i"
                  class="p-2 rounded-lg border-l-4"
                  :style="{
                    borderColor: PRIORITY_INFO[rem.priority]?.color,
                    backgroundColor: PRIORITY_INFO[rem.priority]?.bgColor,
                  }"
                >
                  <div class="text-sm font-medium text-gray-900">{{ rem.action }}</div>
                  <div class="text-xs text-gray-500 mt-1">
                    Responsible: {{ rem.actor }}
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Events List -->
          <div v-if="simState.scenario" class="bg-white rounded-xl border-2 border-gray-300 shadow-md p-4">
            <h3 class="font-bold text-gray-900 mb-3">Timeline Events</h3>
            <div class="space-y-2 max-h-64 overflow-y-auto">
              <button
                v-for="event in sortedEvents"
                :key="`${event.day}-${event.name}`"
                @click="seekToDay(event.day)"
                :class="[
                  'w-full text-left p-2 rounded-lg transition-colors flex items-center gap-2',
                  simState.activeEvent === event
                    ? 'bg-green-100 border border-green-300'
                    : event.day <= simState.currentDay
                      ? 'bg-gray-50 hover:bg-gray-100'
                      : 'opacity-50 hover:opacity-75',
                ]"
              >
                <span class="text-lg">{{ EVENT_TYPE_INFO[event.type]?.icon }}</span>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-medium text-gray-900 truncate">{{ event.name }}</div>
                  <div class="text-xs text-gray-500">Day {{ event.day }}</div>
                </div>
              </button>
            </div>
          </div>

          <!-- Placeholder when no scenario -->
          <div v-else class="bg-white rounded-xl border-2 border-gray-300 shadow-md p-4 text-center text-gray-600">
            <div class="text-4xl mb-2">🎯</div>
            <p class="text-sm font-medium">Select a scenario to explore its timeline and impacts</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Panel (slide-over) -->
    <Teleport to="body">
      <div
        v-if="showChatPanel"
        class="fixed inset-0 z-50"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-black/30"
          @click="showChatPanel = false"
        />

        <!-- Panel -->
        <div class="absolute right-0 top-0 bottom-0 w-full max-w-md bg-white shadow-xl">
          <DisasterChat
            :system-slug="slug"
            @scenario-generated="handleScenarioGenerated"
            @close="showChatPanel = false"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>
