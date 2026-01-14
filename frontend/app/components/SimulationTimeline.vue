<script setup lang="ts">
import type { SimulationScenario, SimulationEvent } from '~/types/simulation'
import { EVENT_TYPE_INFO } from '~/types/simulation'

const props = defineProps<{
  scenario: SimulationScenario | null
  currentDay: number
  isPlaying: boolean
  playbackSpeed: number
}>()

const emit = defineEmits<{
  (e: 'play'): void
  (e: 'pause'): void
  (e: 'stop'): void
  (e: 'seek', day: number): void
  (e: 'speed', speed: number): void
}>()

// Computed properties
const duration = computed(() => props.scenario?.scenario.duration || 100)
const progress = computed(() => (props.currentDay / duration.value) * 100)
const sortedEvents = computed(() => {
  if (!props.scenario) return []
  return [...props.scenario.events].sort((a, b) => a.day - b.day)
})

// Format day display
function formatDay(day: number): string {
  const d = Math.floor(day)
  if (d === 1) return 'Day 1'
  return `Day ${d}`
}

// Get event position on timeline
function getEventPosition(event: SimulationEvent): string {
  return `${(event.day / duration.value) * 100}%`
}

// Handle click on timeline track
function handleTrackClick(event: MouseEvent) {
  const target = event.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()
  const x = event.clientX - rect.left
  const percent = x / rect.width
  const day = Math.round(percent * duration.value)
  emit('seek', day)
}

// Tooltip state
const hoveredEvent = ref<SimulationEvent | null>(null)
const tooltipStyle = ref({ left: '0px', top: '0px' })

function showTooltip(event: SimulationEvent, mouseEvent: MouseEvent) {
  hoveredEvent.value = event
  const target = mouseEvent.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()
  tooltipStyle.value = {
    left: `${rect.left + rect.width / 2}px`,
    top: `${rect.top - 10}px`,
  }
}

function hideTooltip() {
  hoveredEvent.value = null
}
</script>

<template>
  <div class="simulation-timeline">
    <!-- Playback Controls -->
    <div class="flex items-center gap-3 mb-4">
      <!-- Play/Pause -->
      <button
        v-if="!isPlaying"
        @click="emit('play')"
        :disabled="!scenario"
        class="w-10 h-10 rounded-full bg-green-700 text-white flex items-center justify-center hover:bg-green-700/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <svg class="w-5 h-5 ml-0.5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8 5v14l11-7z" />
        </svg>
      </button>
      <button
        v-else
        @click="emit('pause')"
        class="w-10 h-10 rounded-full bg-green-700 text-white flex items-center justify-center hover:bg-green-700/90 transition-colors"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
        </svg>
      </button>

      <!-- Stop/Reset -->
      <button
        @click="emit('stop')"
        :disabled="!scenario"
        class="w-10 h-10 rounded-full border-2 border-gray-400 bg-gray-100 text-gray-700 flex items-center justify-center hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M6 6h12v12H6z" />
        </svg>
      </button>

      <!-- Speed Control -->
      <div class="flex items-center gap-1 ml-2">
        <button
          v-for="speed in [1, 2, 4]"
          :key="speed"
          @click="emit('speed', speed)"
          :class="[
            'px-2 py-1 text-sm rounded font-medium transition-colors',
            playbackSpeed === speed
              ? 'bg-green-700 text-white shadow-sm'
              : 'bg-gray-200 text-gray-700 border border-gray-300 hover:bg-gray-300',
          ]"
        >
          {{ speed }}x
        </button>
      </div>

      <!-- Day Display -->
      <div class="ml-auto text-sm text-gray-700 bg-gray-100 px-3 py-1 rounded border border-gray-300">
        <span class="font-bold">{{ formatDay(currentDay) }}</span>
        <span class="text-gray-500"> / {{ duration }} days</span>
      </div>
    </div>

    <!-- Timeline Track -->
    <div
      class="relative h-12 bg-gray-200 rounded-lg cursor-pointer border border-gray-300"
      @click="handleTrackClick"
    >
      <!-- Progress bar -->
      <div
        class="absolute h-full bg-green-700/30 rounded-l-lg transition-all duration-75"
        :style="{ width: `${progress}%` }"
      />

      <!-- Event markers -->
      <div
        v-for="event in sortedEvents"
        :key="`${event.day}-${event.name}`"
        class="absolute top-1 bottom-1 w-1.5 rounded-full cursor-pointer transition-transform hover:scale-150"
        :style="{
          left: getEventPosition(event),
          backgroundColor: EVENT_TYPE_INFO[event.type]?.color || '#6B7280',
        }"
        @mouseenter="showTooltip(event, $event)"
        @mouseleave="hideTooltip"
        @click.stop="emit('seek', event.day)"
      />

      <!-- Current position indicator -->
      <div
        class="absolute top-0 bottom-0 w-0.5 bg-green-700 z-10 transition-all duration-75"
        :style="{ left: `${progress}%` }"
      >
        <!-- Triangle indicator on top -->
        <div
          class="absolute -top-1 left-1/2 -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-green-700"
        />
      </div>
    </div>

    <!-- Event Tooltip -->
    <Teleport to="body">
      <div
        v-if="hoveredEvent"
        class="fixed z-50 bg-gray-900 text-white text-sm rounded-lg px-3 py-2 shadow-lg -translate-x-1/2 -translate-y-full pointer-events-none"
        :style="tooltipStyle"
      >
        <div class="font-medium flex items-center gap-2">
          <span>{{ EVENT_TYPE_INFO[hoveredEvent.type]?.icon }}</span>
          {{ hoveredEvent.name }}
        </div>
        <div class="text-gray-300 text-xs">
          Day {{ hoveredEvent.day }}
        </div>
        <!-- Arrow -->
        <div
          class="absolute left-1/2 -translate-x-1/2 bottom-0 translate-y-full w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-gray-900"
        />
      </div>
    </Teleport>

    <!-- Events Legend (compact) -->
    <div class="flex flex-wrap gap-x-4 gap-y-1 mt-3 text-xs text-gray-600 font-medium">
      <div
        v-for="(info, type) in EVENT_TYPE_INFO"
        :key="type"
        class="flex items-center gap-1.5"
      >
        <span
          class="w-2.5 h-2.5 rounded-full border border-gray-400"
          :style="{ backgroundColor: info.color }"
        />
        <span>{{ info.label }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.simulation-timeline {
  @apply p-4 bg-white rounded-xl border-2 border-gray-300 shadow-md;
}
</style>
