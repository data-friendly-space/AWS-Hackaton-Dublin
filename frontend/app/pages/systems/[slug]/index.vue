<script setup lang="ts">
import {
  ArrowLeft, Download, Network, Users, AlertTriangle, Link, Bot,
  Send, Sparkles, Component, FileText, Eye, MessageSquare,
  ChevronRight, Info, CheckCircle2, XCircle, AlertCircle,
  ZoomIn, ZoomOut, RotateCcw, LayoutGrid, Upload, Loader2
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

// Auth check for upload permissions
const { isSuperadmin, isR4SManager } = useAuth()
const canUpload = computed(() => isSuperadmin.value || isR4SManager.value)

useHead({
  title: () => system ? `${system.name} - Resilio` : 'System Not Found',
})

// =========================================================================
// Visualization State & Logic
// =========================================================================
const canvasRef = ref<HTMLCanvasElement | null>(null)
const canvasContainerRef = ref<HTMLDivElement | null>(null)
const activeTab = ref('summary')
const activeFilter = ref('all')
const hoveredNode = ref<any>(null)
const selectedNode = ref<any>(null)
const tooltipVisible = ref(false)
const tooltipX = ref(0)
const tooltipY = ref(0)
const visualizationInitialized = ref(false)

// View state
const scale = ref(1)
const offsetX = ref(0)
const offsetY = ref(0)

// Drag state
const dragging = ref(false)
const dragNode = ref<any>(null)
const dragStartX = ref(0)
const dragStartY = ref(0)

// Nodes and edges for visualization
const visNodes = ref<any[]>([])
const visEdges = ref<any[]>([])

// Animation state for pulsing stressed relationships
const animationTime = ref(0)
const animationFrameId = ref<number | null>(null)

// R4S Framework Visualization State
const visualizationMode = ref<'network' | 'r4s'>('network')
const r4sContainerRef = ref<HTMLDivElement | null>(null)
const r4sDotCode = ref<string | null>(null)
const r4sLoading = ref(false)
const r4sError = ref<string | null>(null)
const r4sCached = ref(false)

// PDF Export State
const isExporting = ref(false)

// Actor type colors
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

function initVisualization() {
  if (!canvasRef.value || !canvasContainerRef.value || !system) return

  const canvas = canvasRef.value
  const container = canvasContainerRef.value

  // Get container dimensions
  const containerWidth = container.clientWidth || container.offsetWidth || 800
  const containerHeight = container.clientHeight || container.offsetHeight || 500

  canvas.width = containerWidth
  canvas.height = containerHeight

  // Create nodes from actors
  const actors = system.actors
  const centerX = canvas.width / 2
  const centerY = canvas.height / 2
  const radius = Math.min(centerX, centerY) * 0.6

  visNodes.value = actors.map((actor: any, i: number) => {
    const angle = (i / actors.length) * Math.PI * 2 - Math.PI / 2
    return {
      id: actor.id,
      x: centerX + Math.cos(angle) * radius,
      y: centerY + Math.sin(angle) * radius,
      radius: 35,
      data: actor,
      color: visColors[actor.actor_type] || '#6B7280'
    }
  })

  // Create edges from relationships
  visEdges.value = system.relationships.map((rel: any) => {
    const fromNode = visNodes.value.find(n => n.data.name === rel.from_actor_name)
    const toNode = visNodes.value.find(n => n.data.name === rel.to_actor_name)
    return {
      from: fromNode,
      to: toNode,
      data: rel
    }
  }).filter((e: any) => e.from && e.to)

  // Run force-directed layout
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

function isNodeVisible(node: any) {
  if (activeFilter.value === 'all') return true
  return node.data.actor_type === activeFilter.value
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
    if (!isNodeVisible(edge.from) || !isNodeVisible(edge.to)) continue
    drawEdge(ctx, edge, animationTime.value)
  }

  // Draw nodes
  for (const node of visNodes.value) {
    if (!isNodeVisible(node)) continue
    drawNode(ctx, node)
  }

  ctx.restore()
}

// Animation loop for pulsing stressed relationships
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

function drawNode(ctx: CanvasRenderingContext2D, node: any) {
  const { x, y, radius, data, color } = node
  const isHovered = node === hoveredNode.value
  const isSelected = node === selectedNode.value

  // Node background
  ctx.beginPath()
  ctx.arc(x, y, radius, 0, Math.PI * 2)
  ctx.fillStyle = isHovered || isSelected ? lightenColor(color, 20) : color
  ctx.fill()

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

  const quality = data.quality || 'good'
  let baseColor = visColors[quality] || '#9CA3AF'

  // Thicker lines: good=4, stressed/bad=5, absent=2
  let lineWidth = quality === 'absent' ? 2 : quality === 'good' ? 4 : 5

  // Pulsing animation for stressed and bad relationships
  if (quality === 'stressed' || quality === 'bad') {
    // Create pulsing effect: oscillate opacity between 0.4 and 1.0
    const pulseSpeed = quality === 'bad' ? 4 : 2 // Bad pulses faster
    const pulse = Math.sin(time * pulseSpeed / 1000 * Math.PI) * 0.3 + 0.7
    ctx.globalAlpha = pulse

    // Also pulse the line width slightly
    lineWidth = lineWidth + Math.sin(time * pulseSpeed / 1000 * Math.PI) * 1.5
  } else {
    ctx.globalAlpha = 1
  }

  ctx.strokeStyle = baseColor
  ctx.lineWidth = lineWidth

  if (quality === 'absent') {
    ctx.setLineDash([8, 8])
  } else if (quality === 'stressed') {
    ctx.setLineDash([12, 6]) // Dashed for stressed
  } else {
    ctx.setLineDash([])
  }

  ctx.beginPath()
  ctx.moveTo(startX, startY)
  ctx.lineTo(endX, endY)
  ctx.stroke()

  // Arrow - larger for thicker lines
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
  ctx.globalAlpha = 1 // Reset alpha
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

function onCanvasMouseDown(e: MouseEvent) {
  const rect = canvasRef.value?.getBoundingClientRect()
  if (!rect) return
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top
  const world = screenToWorld(mouseX, mouseY)

  for (const node of visNodes.value) {
    if (!isNodeVisible(node)) continue
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
  const world = screenToWorld(mouseX, mouseY)

  if (dragNode.value) {
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

  // Check hover
  let hovered = null
  for (const node of visNodes.value) {
    if (!isNodeVisible(node)) continue
    const dx = world.x - node.x
    const dy = world.y - node.y
    if (Math.sqrt(dx * dx + dy * dy) < node.radius) {
      hovered = node
      break
    }
  }

  if (hovered !== hoveredNode.value) {
    hoveredNode.value = hovered
    if (hovered) {
      tooltipX.value = mouseX + 15
      tooltipY.value = mouseY + 15
      tooltipVisible.value = true
    } else {
      tooltipVisible.value = false
    }
    renderCanvas()
  }
}

function onCanvasMouseUp() {
  dragging.value = false
  dragNode.value = null
}

function onCanvasWheel(e: WheelEvent) {
  e.preventDefault()
  const rect = canvasRef.value?.getBoundingClientRect()
  if (!rect) return
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top

  const zoom = e.deltaY > 0 ? 0.9 : 1.1
  const newScale = Math.max(0.1, Math.min(5, scale.value * zoom))

  offsetX.value = mouseX - (mouseX - offsetX.value) * (newScale / scale.value)
  offsetY.value = mouseY - (mouseY - offsetY.value) * (newScale / scale.value)
  scale.value = newScale
  renderCanvas()
}

function zoomInVis() {
  scale.value = Math.min(5, scale.value * 1.2)
  renderCanvas()
}

function zoomOutVis() {
  scale.value = Math.max(0.1, scale.value / 1.2)
  renderCanvas()
}

function resetViewVis() {
  centerView()
  renderCanvas()
}

function autoLayoutVis() {
  if (!canvasRef.value || !canvasContainerRef.value) return
  const canvas = canvasRef.value
  const container = canvasContainerRef.value
  canvas.width = container.clientWidth
  canvas.height = container.clientHeight
  runForceLayout()
  renderCanvas()
}

function setFilter(filter: string) {
  activeFilter.value = filter
  renderCanvas()
}

// =========================================================================
// R4S Framework Visualization
// =========================================================================
async function loadR4SVisualization() {
  if (r4sLoading.value) return

  r4sLoading.value = true
  r4sError.value = null

  try {
    const config = useRuntimeConfig()

    // No auth header needed - this endpoint is public
    const response = await $fetch<{ dot: string; cached: boolean }>(`${config.public.apiBase}/agents/visualize/${slug}/`)

    r4sDotCode.value = response.dot
    r4sCached.value = response.cached

    await nextTick()
    await renderR4SVisualization(response.dot)
  } catch (error: any) {
    console.error('Failed to load R4S visualization:', error)
    r4sError.value = error.message || 'Failed to generate visualization'
  } finally {
    r4sLoading.value = false
  }
}

async function regenerateR4SVisualization() {
  if (r4sLoading.value) return

  r4sLoading.value = true
  r4sError.value = null

  try {
    const config = useRuntimeConfig()

    // No auth header needed - this endpoint is public
    const response = await $fetch<{ dot: string }>(`${config.public.apiBase}/agents/visualize/${slug}/`, {
      method: 'POST'
    })

    r4sDotCode.value = response.dot
    r4sCached.value = false

    await nextTick()
    await renderR4SVisualization(response.dot)
  } catch (error: any) {
    console.error('Failed to regenerate R4S visualization:', error)
    r4sError.value = error.message || 'Failed to regenerate visualization'
  } finally {
    r4sLoading.value = false
  }
}

async function renderR4SVisualization(dotCode: string) {
  if (!r4sContainerRef.value) return

  try {
    // Dynamically import viz.js (WASM-based Graphviz)
    const { instance } = await import('@viz-js/viz')
    const viz = await instance()

    // Clear previous content
    r4sContainerRef.value.innerHTML = ''

    // Render DOT to SVG
    const svg = viz.renderSVGElement(dotCode)

    // Make SVG responsive
    svg.setAttribute('width', '100%')
    svg.setAttribute('height', '100%')
    svg.style.maxWidth = '100%'
    svg.style.maxHeight = '100%'

    r4sContainerRef.value.appendChild(svg)
  } catch (error: any) {
    console.error('Failed to render Graphviz:', error)
    r4sError.value = 'Failed to render visualization: ' + (error.message || 'Unknown error')
  }
}

function switchVisualizationMode(mode: 'network' | 'r4s') {
  visualizationMode.value = mode

  if (mode === 'r4s') {
    stopAnimation() // Stop network graph animation when switching to R4S
    if (!r4sDotCode.value && !r4sLoading.value) {
      loadR4SVisualization()
    }
  } else if (mode === 'network') {
    if (!visualizationInitialized.value) {
      nextTick(() => tryInitVisualization())
    } else {
      startAnimation() // Restart animation when switching back to network
    }
  }
}

// Cleanup animation on component unmount
onUnmounted(() => {
  stopAnimation()
})

// Try to initialize visualization - will retry if container not ready
function tryInitVisualization() {
  if (visualizationInitialized.value) return

  if (!canvasRef.value || !canvasContainerRef.value) {
    return // Elements not in DOM yet
  }

  const container = canvasContainerRef.value
  const width = container.clientWidth || container.offsetWidth
  const height = container.clientHeight || container.offsetHeight

  if (width > 100 && height > 100) {
    initVisualization()
    visualizationInitialized.value = true
    startAnimation() // Start animation for pulsing stressed relationships
  }
}

// Initialize visualization when tab becomes visible
watch(activeTab, (newTab) => {
  if (newTab === 'visualization' && !visualizationInitialized.value) {
    // Try immediately, then retry a few times
    nextTick(() => {
      tryInitVisualization()
      // Retry a few times in case DOM isn't ready
      const retryTimes = [100, 200, 500, 1000]
      retryTimes.forEach(delay => {
        setTimeout(tryInitVisualization, delay)
      })
    })
  }
})

// Also watch for canvas ref becoming available (backup initialization)
watch(canvasRef, (newCanvas) => {
  if (newCanvas && activeTab.value === 'visualization' && !visualizationInitialized.value) {
    nextTick(() => {
      tryInitVisualization()
      setTimeout(tryInitVisualization, 100)
    })
  }
})

// Also handle window resize for the visualization
onMounted(() => {
  if (import.meta.client) {
    window.addEventListener('resize', () => {
      if (activeTab.value === 'visualization' && canvasRef.value && canvasContainerRef.value) {
        canvasRef.value.width = canvasContainerRef.value.clientWidth
        canvasRef.value.height = canvasContainerRef.value.clientHeight
        renderCanvas()
      }
    })
  }
})

// =========================================================================
// PDF Export Function
// =========================================================================
async function exportToPDF() {
  if (!system || isExporting.value) return

  isExporting.value = true

  try {
    // Dynamically import jsPDF (client-side only)
    const { default: jsPDF } = await import('jspdf')
    const { default: autoTable } = await import('jspdf-autotable')

    // Create PDF document (A4 size)
    const doc = new jsPDF('p', 'mm', 'a4')
    const pageWidth = doc.internal.pageSize.getWidth()
    const pageHeight = doc.internal.pageSize.getHeight()
    const margin = 15
    let yPos = margin

    // Helper function to add new page if needed
    const checkNewPage = (neededHeight: number) => {
      if (yPos + neededHeight > pageHeight - margin) {
        doc.addPage()
        yPos = margin
        return true
      }
      return false
    }

    // ===== HEADER =====
    // GOAL Green header bar
    doc.setFillColor(0, 110, 51) // GOAL green
    doc.rect(0, 0, pageWidth, 25, 'F')

    // Title
    doc.setTextColor(255, 255, 255)
    doc.setFontSize(18)
    doc.setFont('helvetica', 'bold')
    doc.text('R4S System Assessment Report', margin, 16)

    // Subtitle with date
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    doc.text(`Generated: ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}`, pageWidth - margin, 16, { align: 'right' })

    yPos = 35

    // ===== SYSTEM INFO =====
    doc.setTextColor(0, 0, 0)
    doc.setFontSize(16)
    doc.setFont('helvetica', 'bold')
    doc.text(system.name, margin, yPos)
    yPos += 8

    // Metadata badges
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    doc.setTextColor(100, 100, 100)
    const metaText = [system.sector_display, system.subsector, system.region, system.country].filter(Boolean).join(' | ')
    doc.text(metaText, margin, yPos)
    yPos += 8

    // Description
    if (system.description) {
      doc.setTextColor(60, 60, 60)
      doc.setFontSize(10)
      const descLines = doc.splitTextToSize(system.description, pageWidth - 2 * margin)
      doc.text(descLines, margin, yPos)
      yPos += descLines.length * 5 + 5
    }

    // ===== KEY METRICS BOX =====
    checkNewPage(35)
    doc.setFillColor(240, 253, 244) // Light green background
    doc.roundedRect(margin, yPos, pageWidth - 2 * margin, 30, 3, 3, 'F')

    // Metrics
    const metricsY = yPos + 12
    const colWidth = (pageWidth - 2 * margin) / 5

    const metrics = [
      { label: 'Actors', value: system.actor_count.toString() },
      { label: 'Relationships', value: system.relationship_count.toString() },
      { label: 'Components', value: system.component_count.toString() },
      { label: 'Risk Scenarios', value: system.risk_count.toString() },
      { label: 'Resilience', value: `${system.resilience_score}%` },
    ]

    metrics.forEach((metric, i) => {
      const x = margin + colWidth * i + colWidth / 2
      doc.setFontSize(16)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(0, 110, 51)
      doc.text(metric.value, x, metricsY, { align: 'center' })
      doc.setFontSize(8)
      doc.setFont('helvetica', 'normal')
      doc.setTextColor(100, 100, 100)
      doc.text(metric.label, x, metricsY + 7, { align: 'center' })
    })

    yPos += 40

    // ===== AI SUMMARY =====
    checkNewPage(50)
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 110, 51)
    doc.text('AI-Generated Analysis', margin, yPos)
    yPos += 8

    doc.setFontSize(9)
    doc.setFont('helvetica', 'normal')
    doc.setTextColor(60, 60, 60)

    // Clean and wrap AI summary text
    const cleanSummary = system.ai_summary
      .replace(/##\s*/g, '')
      .replace(/###\s*/g, '')
      .replace(/\*\*/g, '')
      .replace(/\n\n/g, '\n')
    const summaryLines = doc.splitTextToSize(cleanSummary, pageWidth - 2 * margin)

    // Limit summary to prevent overflow
    const maxSummaryLines = Math.min(summaryLines.length, 25)
    for (let i = 0; i < maxSummaryLines; i++) {
      if (checkNewPage(5)) {
        // Add section header on new page
      }
      doc.text(summaryLines[i], margin, yPos)
      yPos += 4.5
    }
    if (summaryLines.length > maxSummaryLines) {
      doc.text('...', margin, yPos)
      yPos += 5
    }
    yPos += 5

    // ===== ACTORS TABLE =====
    checkNewPage(40)
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 110, 51)
    doc.text('System Actors', margin, yPos)
    yPos += 6

    const actorRows = system.actors.map((actor: any) => [
      actor.name,
      actor.actor_type_display,
      actor.function?.substring(0, 80) + (actor.function?.length > 80 ? '...' : '')
    ])

    autoTable(doc, {
      startY: yPos,
      head: [['Actor Name', 'Type', 'Function']],
      body: actorRows,
      margin: { left: margin, right: margin },
      headStyles: { fillColor: [0, 110, 51], fontSize: 9 },
      bodyStyles: { fontSize: 8 },
      columnStyles: {
        0: { cellWidth: 45 },
        1: { cellWidth: 30 },
        2: { cellWidth: 'auto' }
      },
      theme: 'striped'
    })

    yPos = (doc as any).lastAutoTable.finalY + 10

    // ===== RELATIONSHIPS TABLE =====
    checkNewPage(40)
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 110, 51)
    doc.text('Relationships', margin, yPos)
    yPos += 6

    const relationshipRows = system.relationships.map((rel: any) => [
      rel.from_actor_name,
      rel.to_actor_name,
      rel.goods_services?.substring(0, 50) + (rel.goods_services?.length > 50 ? '...' : ''),
      rel.quality_display
    ])

    autoTable(doc, {
      startY: yPos,
      head: [['From Actor', 'To Actor', 'Goods/Services', 'Quality']],
      body: relationshipRows,
      margin: { left: margin, right: margin },
      headStyles: { fillColor: [0, 110, 51], fontSize: 9 },
      bodyStyles: { fontSize: 8 },
      columnStyles: {
        0: { cellWidth: 40 },
        1: { cellWidth: 40 },
        2: { cellWidth: 'auto' },
        3: { cellWidth: 25 }
      },
      theme: 'striped',
      didParseCell: (data: any) => {
        // Color code quality column
        if (data.column.index === 3 && data.section === 'body') {
          const quality = system.relationships[data.row.index]?.quality
          if (quality === 'good') data.cell.styles.textColor = [34, 197, 94]
          else if (quality === 'stressed') data.cell.styles.textColor = [245, 158, 11]
          else if (quality === 'bad') data.cell.styles.textColor = [239, 68, 68]
          else if (quality === 'absent') data.cell.styles.textColor = [156, 163, 175]
        }
      }
    })

    yPos = (doc as any).lastAutoTable.finalY + 10

    // ===== RISK SCENARIOS TABLE =====
    checkNewPage(40)
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 110, 51)
    doc.text('Risk Scenarios', margin, yPos)
    yPos += 6

    const riskRows = system.risks.map((risk: any) => [
      risk.name,
      risk.category_display,
      risk.likelihood_display,
      risk.description?.substring(0, 60) + (risk.description?.length > 60 ? '...' : '')
    ])

    autoTable(doc, {
      startY: yPos,
      head: [['Risk', 'Category', 'Likelihood', 'Description']],
      body: riskRows,
      margin: { left: margin, right: margin },
      headStyles: { fillColor: [0, 110, 51], fontSize: 9 },
      bodyStyles: { fontSize: 8 },
      columnStyles: {
        0: { cellWidth: 40 },
        1: { cellWidth: 25 },
        2: { cellWidth: 25 },
        3: { cellWidth: 'auto' }
      },
      theme: 'striped'
    })

    yPos = (doc as any).lastAutoTable.finalY + 10

    // ===== COMPONENTS TABLE =====
    checkNewPage(40)
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 110, 51)
    doc.text('System Components', margin, yPos)
    yPos += 6

    const componentRows = system.components.map((comp: any) => [
      comp.name,
      comp.category_display,
      comp.status_display,
      comp.description?.substring(0, 50) + (comp.description?.length > 50 ? '...' : '')
    ])

    autoTable(doc, {
      startY: yPos,
      head: [['Component', 'Category', 'Status', 'Description']],
      body: componentRows,
      margin: { left: margin, right: margin },
      headStyles: { fillColor: [0, 110, 51], fontSize: 9 },
      bodyStyles: { fontSize: 8 },
      columnStyles: {
        0: { cellWidth: 45 },
        1: { cellWidth: 30 },
        2: { cellWidth: 25 },
        3: { cellWidth: 'auto' }
      },
      theme: 'striped',
      didParseCell: (data: any) => {
        // Color code status column
        if (data.column.index === 2 && data.section === 'body') {
          const status = system.components[data.row.index]?.status
          if (status === 'functional') data.cell.styles.textColor = [34, 197, 94]
          else if (status === 'degraded') data.cell.styles.textColor = [245, 158, 11]
          else if (status === 'non_functional') data.cell.styles.textColor = [239, 68, 68]
        }
      }
    })

    yPos = (doc as any).lastAutoTable.finalY + 10

    // ===== NETWORK GRAPH VISUALIZATION =====
    // Ensure the network graph is initialized
    if (canvasRef.value && canvasContainerRef.value) {
      // Initialize visualization if not already done
      if (!visualizationInitialized.value) {
        initVisualization()
        renderCanvas()
        // Small delay to ensure rendering is complete
        await new Promise(resolve => setTimeout(resolve, 100))
      }

      // Only add if canvas has content
      if (canvasRef.value.width > 0 && canvasRef.value.height > 0) {
        doc.addPage()
        yPos = margin

        doc.setFontSize(14)
        doc.setFont('helvetica', 'bold')
        doc.setTextColor(0, 110, 51)
        doc.text('Network Graph Visualization', margin, yPos)
        yPos += 10

        try {
          const imgData = canvasRef.value.toDataURL('image/png')
          const pageWidth = doc.internal.pageSize.getWidth()
          const pageHeight = doc.internal.pageSize.getHeight()

          const maxWidth = pageWidth - 2 * margin
          const maxHeight = pageHeight - yPos - margin - 10
          const canvasWidth = canvasRef.value.width
          const canvasHeight = canvasRef.value.height
          const imgScale = Math.min(maxWidth / canvasWidth, maxHeight / canvasHeight)
          const imgWidth = canvasWidth * imgScale
          const imgHeight = canvasHeight * imgScale

          const xOffset = (pageWidth - imgWidth) / 2
          doc.addImage(imgData, 'PNG', xOffset, yPos, imgWidth, imgHeight)

          // Add legend
          yPos += imgHeight + 10
          doc.setFontSize(9)
          doc.setFont('helvetica', 'normal')
          doc.setTextColor(100, 100, 100)

          const legendItems = [
            { color: [139, 92, 246], label: 'Service Users' },
            { color: [0, 110, 51], label: 'Service Providers' },
            { color: [245, 158, 11], label: 'Support Actors' },
            { color: [239, 68, 68], label: 'Regulatory Bodies' }
          ]

          let legendX = margin
          legendItems.forEach((item) => {
            doc.setFillColor(item.color[0], item.color[1], item.color[2])
            doc.circle(legendX + 3, yPos, 3, 'F')
            doc.text(item.label, legendX + 8, yPos + 1)
            legendX += 45
          })
        } catch (e) {
          console.error('Failed to add network graph to PDF:', e)
        }
      }
    }

    // ===== R4S VISUALIZATION =====
    // Use viz.js to render DOT code directly to canvas for PDF
    if (r4sDotCode.value) {
      doc.addPage('landscape')
      yPos = margin

      doc.setFontSize(14)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(0, 110, 51)
      doc.text('R4S Framework Visualization', margin, yPos)
      yPos += 10

      try {
        // Import viz.js and render DOT to SVG
        const { instance } = await import('@viz-js/viz')
        const viz = await instance()
        const svgString = viz.renderString(r4sDotCode.value, { format: 'svg' })

        // Create a temporary container for the SVG
        const tempDiv = document.createElement('div')
        tempDiv.innerHTML = svgString
        const svgElement = tempDiv.querySelector('svg')

        if (svgElement) {
          // Get SVG dimensions
          const svgWidth = parseFloat(svgElement.getAttribute('width') || '800')
          const svgHeight = parseFloat(svgElement.getAttribute('height') || '600')

          // Create canvas and draw SVG
          const canvas = document.createElement('canvas')
          const scaleFactor = 2 // Higher resolution
          canvas.width = svgWidth * scaleFactor
          canvas.height = svgHeight * scaleFactor
          const ctx = canvas.getContext('2d')

          if (ctx) {
            // Draw white background
            ctx.fillStyle = 'white'
            ctx.fillRect(0, 0, canvas.width, canvas.height)

            // Convert SVG to data URL with proper encoding
            const svgData = new XMLSerializer().serializeToString(svgElement)
            const svgBase64 = btoa(unescape(encodeURIComponent(svgData)))
            const svgDataUrl = 'data:image/svg+xml;base64,' + svgBase64

            // Load image and draw to canvas
            await new Promise<void>((resolve, reject) => {
              const img = new Image()
              img.onload = () => {
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
                resolve()
              }
              img.onerror = () => {
                console.error('Failed to load SVG image')
                reject(new Error('SVG load failed'))
              }
              img.src = svgDataUrl
            })

            // Add to PDF
            const imgData = canvas.toDataURL('image/png')
            const landscapeWidth = doc.internal.pageSize.getWidth()
            const landscapeHeight = doc.internal.pageSize.getHeight()

            const maxWidth = landscapeWidth - 2 * margin
            const maxHeight = landscapeHeight - yPos - margin
            const imgScale = Math.min(maxWidth / svgWidth, maxHeight / svgHeight)
            const imgWidth = svgWidth * imgScale
            const imgHeight = svgHeight * imgScale

            doc.addImage(imgData, 'PNG', margin, yPos, imgWidth, imgHeight)
          }
        }
      } catch (e) {
        console.error('Failed to add R4S visualization to PDF:', e)
        doc.setFontSize(10)
        doc.setTextColor(150, 150, 150)
        doc.text('(R4S visualization could not be embedded - view in web application)', margin, yPos + 10)
      }
    }

    // ===== FOOTER ON ALL PAGES =====
    const totalPages = doc.getNumberOfPages()
    for (let i = 1; i <= totalPages; i++) {
      doc.setPage(i)
      const currentPageHeight = doc.internal.pageSize.getHeight()
      const currentPageWidth = doc.internal.pageSize.getWidth()

      // Footer line
      doc.setDrawColor(200, 200, 200)
      doc.line(margin, currentPageHeight - 12, currentPageWidth - margin, currentPageHeight - 12)

      // Footer text
      doc.setFontSize(8)
      doc.setTextColor(150, 150, 150)
      doc.text('Generated by Resilio - R4S System Mapping Tool', margin, currentPageHeight - 7)
      doc.text(`Page ${i} of ${totalPages}`, currentPageWidth - margin, currentPageHeight - 7, { align: 'right' })
    }

    // Save the PDF
    const filename = `${system.slug}-r4s-report-${new Date().toISOString().split('T')[0]}.pdf`
    doc.save(filename)

  } catch (error) {
    console.error('Failed to generate PDF:', error)
    alert('Failed to generate PDF report. Please try again.')
  } finally {
    isExporting.value = false
  }
}

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
          <div class="flex gap-2">
            <NuxtLink v-if="canUpload" :to="`/systems/${slug}/upload`">
              <Button variant="outline">
                <Upload class="mr-2 h-4 w-4" />
                Upload Data
              </Button>
            </NuxtLink>
            <Button variant="outline" @click="exportToPDF" :disabled="isExporting">
              <Loader2 v-if="isExporting" class="mr-2 h-4 w-4 animate-spin" />
              <Download v-else class="mr-2 h-4 w-4" />
              {{ isExporting ? 'Generating...' : 'Export Report' }}
            </Button>
          </div>
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
      <Tabs v-model="activeTab" class="w-full">
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
                Interactive visualization of actors, relationships, and system components. Drag nodes to reposition, scroll to zoom, pan by dragging background.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <!-- Visualization Mode Toggle -->
              <div class="flex gap-2 mb-4">
                <button
                  :class="['px-4 py-2 text-sm font-medium rounded-lg border transition-all', visualizationMode === 'network' ? 'bg-goal text-white border-goal' : 'bg-white text-gray-700 border-gray-300 hover:border-goal']"
                  @click="switchVisualizationMode('network')"
                >
                  Network Graph
                </button>
                <button
                  :class="['px-4 py-2 text-sm font-medium rounded-lg border transition-all', visualizationMode === 'r4s' ? 'bg-goal text-white border-goal' : 'bg-white text-gray-700 border-gray-300 hover:border-goal']"
                  @click="switchVisualizationMode('r4s')"
                >
                  R4S Framework
                </button>
              </div>

              <!-- Network Graph Visualization -->
              <div v-show="visualizationMode === 'network'">
              <!-- Canvas Container -->
              <div ref="canvasContainerRef" class="relative rounded-xl border bg-slate-100 overflow-hidden h-[500px]" @click="!visualizationInitialized && tryInitVisualization()">
                <!-- Loading state -->
                <div v-if="!visualizationInitialized && activeTab === 'visualization'" class="absolute inset-0 flex items-center justify-center bg-slate-100 z-10">
                  <div class="text-center">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-goal mx-auto mb-2"></div>
                    <p class="text-sm text-muted-foreground">Loading visualization...</p>
                    <button @click.stop="tryInitVisualization()" class="mt-2 text-xs text-goal underline">Click to retry</button>
                  </div>
                </div>
                <canvas
                  ref="canvasRef"
                  class="block w-full h-full cursor-grab"
                  @mousedown="onCanvasMouseDown"
                  @mousemove="onCanvasMouseMove"
                  @mouseup="onCanvasMouseUp"
                  @mouseleave="onCanvasMouseUp"
                  @wheel="onCanvasWheel"
                ></canvas>

                <!-- Filter Bar -->
                <div class="absolute top-4 left-4 flex flex-wrap gap-2">
                  <button
                    :class="['px-3 py-1.5 text-xs font-medium rounded-full border shadow-sm transition-all', activeFilter === 'all' ? 'bg-goal text-white border-goal' : 'bg-white text-gray-700 border-gray-300 hover:border-goal']"
                    @click="setFilter('all')"
                  >
                    All Actors
                  </button>
                  <button
                    :class="['px-3 py-1.5 text-xs font-medium rounded-full border shadow-sm transition-all flex items-center gap-1.5', activeFilter === 'service_user' ? 'bg-violet-500 text-white border-violet-500' : 'bg-white text-gray-700 border-gray-300 hover:border-violet-500']"
                    @click="setFilter('service_user')"
                  >
                    <span class="w-2 h-2 rounded-full bg-violet-500" :class="{ 'bg-white': activeFilter === 'service_user' }"></span>
                    Users
                  </button>
                  <button
                    :class="['px-3 py-1.5 text-xs font-medium rounded-full border shadow-sm transition-all flex items-center gap-1.5', activeFilter === 'service_provider' ? 'bg-goal text-white border-goal' : 'bg-white text-gray-700 border-gray-300 hover:border-goal']"
                    @click="setFilter('service_provider')"
                  >
                    <span class="w-2 h-2 rounded-full bg-goal" :class="{ 'bg-white': activeFilter === 'service_provider' }"></span>
                    Providers
                  </button>
                  <button
                    :class="['px-3 py-1.5 text-xs font-medium rounded-full border shadow-sm transition-all flex items-center gap-1.5', activeFilter === 'support' ? 'bg-amber-500 text-white border-amber-500' : 'bg-white text-gray-700 border-gray-300 hover:border-amber-500']"
                    @click="setFilter('support')"
                  >
                    <span class="w-2 h-2 rounded-full bg-amber-500" :class="{ 'bg-white': activeFilter === 'support' }"></span>
                    Support
                  </button>
                  <button
                    :class="['px-3 py-1.5 text-xs font-medium rounded-full border shadow-sm transition-all flex items-center gap-1.5', activeFilter === 'regulatory' ? 'bg-red-500 text-white border-red-500' : 'bg-white text-gray-700 border-gray-300 hover:border-red-500']"
                    @click="setFilter('regulatory')"
                  >
                    <span class="w-2 h-2 rounded-full bg-red-500" :class="{ 'bg-white': activeFilter === 'regulatory' }"></span>
                    Regulatory
                  </button>
                </div>

                <!-- Zoom Controls -->
                <div class="absolute bottom-4 right-4 flex flex-col gap-2">
                  <button
                    class="w-10 h-10 rounded-lg bg-white border border-gray-300 shadow-sm flex items-center justify-center hover:bg-gray-50 hover:border-goal transition-all"
                    @click="zoomInVis"
                    title="Zoom In"
                  >
                    <ZoomIn class="w-5 h-5 text-gray-700" />
                  </button>
                  <button
                    class="w-10 h-10 rounded-lg bg-white border border-gray-300 shadow-sm flex items-center justify-center hover:bg-gray-50 hover:border-goal transition-all"
                    @click="zoomOutVis"
                    title="Zoom Out"
                  >
                    <ZoomOut class="w-5 h-5 text-gray-700" />
                  </button>
                  <button
                    class="w-10 h-10 rounded-lg bg-white border border-gray-300 shadow-sm flex items-center justify-center hover:bg-gray-50 hover:border-goal transition-all"
                    @click="resetViewVis"
                    title="Reset View"
                  >
                    <RotateCcw class="w-5 h-5 text-gray-700" />
                  </button>
                  <button
                    class="w-10 h-10 rounded-lg bg-white border border-gray-300 shadow-sm flex items-center justify-center hover:bg-gray-50 hover:border-goal transition-all"
                    @click="autoLayoutVis"
                    title="Auto Layout"
                  >
                    <LayoutGrid class="w-5 h-5 text-gray-700" />
                  </button>
                </div>

                <!-- Tooltip -->
                <div
                  v-if="tooltipVisible && hoveredNode"
                  class="absolute bg-gray-900 text-white px-3 py-2 rounded-lg text-sm pointer-events-none z-50 shadow-lg"
                  :style="{ left: tooltipX + 'px', top: tooltipY + 'px' }"
                >
                  <div class="font-semibold">{{ hoveredNode.data.name }}</div>
                  <div class="text-xs text-gray-400 uppercase">{{ hoveredNode.data.actor_type_display }}</div>
                </div>
              </div>

              <!-- Selected Node Details -->
              <div v-if="selectedNode" class="mt-4 p-4 bg-muted rounded-lg">
                <div class="flex items-start gap-3">
                  <div
                    class="w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold"
                    :style="{ backgroundColor: selectedNode.color }"
                  >
                    {{ selectedNode.data.name?.charAt(0) || '?' }}
                  </div>
                  <div class="flex-1">
                    <h4 class="font-semibold">{{ selectedNode.data.name }}</h4>
                    <p class="text-sm text-muted-foreground">{{ selectedNode.data.actor_type_display }}</p>
                    <p class="text-sm mt-2">{{ selectedNode.data.function }}</p>
                  </div>
                </div>
              </div>

              <!-- Legend -->
              <div class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded-full" style="background-color: #8B5CF6;"></div>
                  <span class="text-sm">Service User</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded-full" style="background-color: #006e33;"></div>
                  <span class="text-sm">Service Provider</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded-full" style="background-color: #F59E0B;"></div>
                  <span class="text-sm">Support</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded-full" style="background-color: #EF4444;"></div>
                  <span class="text-sm">Regulatory</span>
                </div>
              </div>
              <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center gap-2">
                  <div class="w-6 h-0.5 rounded" style="background-color: #22C55E;"></div>
                  <span class="text-sm">Good</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-6 h-0.5 rounded" style="background-color: #F59E0B;"></div>
                  <span class="text-sm">Stressed</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-6 h-0.5 rounded" style="background-color: #EF4444;"></div>
                  <span class="text-sm">Bad</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-6 h-0.5 rounded border border-dashed border-gray-400"></div>
                  <span class="text-sm">Absent</span>
                </div>
              </div>
              </div>

              <!-- R4S Framework Visualization -->
              <div v-show="visualizationMode === 'r4s'">
                <!-- R4S Container -->
                <div class="relative rounded-xl border bg-white overflow-hidden min-h-[500px]">
                  <!-- Loading state -->
                  <div v-if="r4sLoading" class="absolute inset-0 flex items-center justify-center bg-white z-10">
                    <div class="text-center">
                      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-goal mx-auto mb-2"></div>
                      <p class="text-sm text-muted-foreground">Generating R4S visualization...</p>
                      <p class="text-xs text-muted-foreground mt-1">This may take a few seconds</p>
                    </div>
                  </div>

                  <!-- Error state -->
                  <div v-else-if="r4sError" class="absolute inset-0 flex items-center justify-center bg-white z-10">
                    <div class="text-center">
                      <div class="text-red-500 text-4xl mb-2">!</div>
                      <p class="text-sm text-red-600 font-medium">Failed to generate visualization</p>
                      <p class="text-xs text-muted-foreground mt-1">{{ r4sError }}</p>
                      <button
                        class="mt-4 px-4 py-2 text-sm font-medium text-white bg-goal rounded-lg hover:bg-goal/90"
                        @click="regenerateR4SVisualization"
                      >
                        Try Again
                      </button>
                    </div>
                  </div>

                  <!-- SVG Container -->
                  <div
                    ref="r4sContainerRef"
                    class="w-full overflow-auto p-4"
                    :class="{ 'opacity-0': r4sLoading || r4sError }"
                  ></div>

                  <!-- Regenerate button -->
                  <div v-if="r4sDotCode && !r4sLoading && !r4sError" class="absolute top-4 right-4">
                    <button
                      class="px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:border-goal hover:text-goal transition-all flex items-center gap-1.5"
                      @click="regenerateR4SVisualization"
                      title="Regenerate visualization"
                    >
                      <RotateCcw class="w-3.5 h-3.5" />
                      Regenerate
                    </button>
                  </div>

                  <!-- Cache indicator -->
                  <div v-if="r4sCached && !r4sLoading && !r4sError" class="absolute bottom-4 left-4">
                    <span class="px-2 py-1 text-xs text-gray-500 bg-gray-100 rounded">
                      Cached visualization
                    </span>
                  </div>
                </div>

                <!-- R4S Legend -->
                <div class="mt-6">
                  <h4 class="text-sm font-semibold mb-3">R4S Three-Tier Framework</h4>
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div class="p-3 bg-amber-50 border border-amber-200 rounded-lg">
                      <div class="font-medium text-amber-700">Top Tier - Supporting Functions</div>
                      <div class="text-xs text-amber-600 mt-1">Leadership, HR, Supplies, Financing</div>
                    </div>
                    <div class="p-3 bg-green-50 border border-green-200 rounded-lg">
                      <div class="font-medium text-green-700">Middle Tier - Core Service Delivery</div>
                      <div class="text-xs text-green-600 mt-1">National to Community level services</div>
                    </div>
                    <div class="p-3 bg-red-50 border border-red-200 rounded-lg">
                      <div class="font-medium text-red-700">Bottom Tier - Regulatory/Normative</div>
                      <div class="text-xs text-red-600 mt-1">Regulators, Cultural influences, Service users</div>
                    </div>
                  </div>
                </div>

                <!-- Connection types legend -->
                <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div class="flex items-center gap-2">
                    <div class="w-6 h-0.5 rounded border-b-2 border-dashed" style="border-color: #3B82F6;"></div>
                    <span class="text-sm">Resources Flow</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <div class="w-6 h-0.5 rounded" style="background-color: #22C55E;"></div>
                    <span class="text-sm">Patient Referrals</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <div class="w-6 h-0.5 rounded border-b-2 border-dotted" style="border-color: #EF4444;"></div>
                    <span class="text-sm">Regulation/Oversight</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <div class="w-6 h-0.5 rounded" style="background-color: #6B7280;"></div>
                    <span class="text-sm">General</span>
                  </div>
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
