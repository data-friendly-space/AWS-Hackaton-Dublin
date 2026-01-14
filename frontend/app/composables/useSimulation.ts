/**
 * Simulation composable for managing risk simulation state and playback
 */

import type {
  SimulationScenario,
  SimulationEvent,
  SimulationState,
  ActorOverride,
  RelationshipOverride,
  QualityState,
  SavedScenario,
  SimulateResponse,
  ChatResponse,
  ChatMessage,
} from '~/types/simulation'

export function useSimulation(systemSlug: Ref<string>) {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBase

  // Simulation state
  const state = reactive<SimulationState>({
    scenario: null,
    currentDay: 0,
    isPlaying: false,
    playbackSpeed: 1,
    actorOverrides: new Map(),
    relationshipOverrides: new Map(),
    activeEvent: null,
  })

  // Playback animation frame
  let animationFrame: number | null = null
  let lastFrameTime = 0

  // Days per second at 1x speed
  const DAYS_PER_SECOND = 2

  /**
   * Load a scenario into the simulation
   */
  function loadScenario(scenario: SimulationScenario) {
    state.scenario = scenario
    state.currentDay = 0
    state.isPlaying = false
    state.actorOverrides.clear()
    state.relationshipOverrides.clear()
    state.activeEvent = null
    computeStateAtDay(0)
  }

  /**
   * Clear the current scenario
   */
  function clearScenario() {
    stop()
    state.scenario = null
    state.currentDay = 0
    state.actorOverrides.clear()
    state.relationshipOverrides.clear()
    state.activeEvent = null
  }

  /**
   * Compute actor/relationship overrides at a given day
   * by applying all events up to and including that day
   */
  function computeStateAtDay(day: number) {
    state.actorOverrides.clear()
    state.relationshipOverrides.clear()
    state.activeEvent = null

    if (!state.scenario) return

    // Sort events by day
    const sortedEvents = [...state.scenario.events].sort((a, b) => a.day - b.day)

    // Apply all events up to current day
    for (const event of sortedEvents) {
      if (event.day > day) break

      // Track the most recent event as active
      if (event.day === Math.floor(day)) {
        state.activeEvent = event
      }

      // Apply impacts
      for (const impact of event.impacts) {
        if (impact.actor) {
          applyActorImpact(impact.actor, impact.attribute, impact.to)
        }
        if (impact.relationship) {
          applyRelationshipImpact(impact.relationship, impact.attribute, impact.to)
        }
      }
    }
  }

  /**
   * Apply an impact to actors matching a pattern
   */
  function applyActorImpact(
    pattern: string,
    attribute: 'quality' | 'active',
    value: QualityState | boolean
  ) {
    // Store the override (pattern matching happens at render time)
    const existing = state.actorOverrides.get(pattern) || {}
    if (attribute === 'quality') {
      existing.quality = value as QualityState
    } else {
      existing.active = value as boolean
    }
    state.actorOverrides.set(pattern, existing)
  }

  /**
   * Apply an impact to relationships matching a pattern
   */
  function applyRelationshipImpact(
    pattern: string,
    attribute: 'quality' | 'active',
    value: QualityState | boolean
  ) {
    if (attribute === 'quality') {
      const existing = state.relationshipOverrides.get(pattern) || {}
      existing.quality = value as QualityState
      state.relationshipOverrides.set(pattern, existing)
    }
  }

  /**
   * Check if an actor slug matches a pattern
   */
  function matchesPattern(slug: string, pattern: string): boolean {
    if (pattern === slug) return true
    if (pattern.endsWith('*')) {
      const prefix = pattern.slice(0, -1)
      return slug.startsWith(prefix)
    }
    return false
  }

  /**
   * Get effective quality for an actor, considering overrides
   */
  function getActorQuality(slug: string, baseQuality: QualityState): QualityState {
    for (const [pattern, override] of state.actorOverrides) {
      if (matchesPattern(slug, pattern) && override.quality) {
        return override.quality
      }
    }
    return baseQuality
  }

  /**
   * Check if an actor is active, considering overrides
   */
  function isActorActive(slug: string): boolean {
    for (const [pattern, override] of state.actorOverrides) {
      if (matchesPattern(slug, pattern) && override.active !== undefined) {
        return override.active
      }
    }
    return true
  }

  /**
   * Get effective quality for a relationship, considering overrides
   */
  function getRelationshipQuality(
    fromSlug: string,
    toSlug: string,
    baseQuality: QualityState
  ): QualityState {
    for (const [pattern, override] of state.relationshipOverrides) {
      // Parse pattern like "from-slug -> to-slug"
      const [fromPattern, toPattern] = pattern.split(' -> ').map(s => s.trim())
      if (
        matchesPattern(fromSlug, fromPattern) &&
        matchesPattern(toSlug, toPattern) &&
        override.quality
      ) {
        return override.quality
      }
    }
    return baseQuality
  }

  /**
   * Animation loop for playback
   */
  function animate(currentTime: number) {
    if (!state.isPlaying || !state.scenario) {
      animationFrame = null
      return
    }

    if (lastFrameTime === 0) {
      lastFrameTime = currentTime
    }

    const deltaTime = (currentTime - lastFrameTime) / 1000 // seconds
    lastFrameTime = currentTime

    // Advance day based on playback speed
    const dayAdvance = deltaTime * DAYS_PER_SECOND * state.playbackSpeed
    const newDay = state.currentDay + dayAdvance

    // Check if we've reached the end
    if (newDay >= state.scenario.scenario.duration) {
      state.currentDay = state.scenario.scenario.duration
      state.isPlaying = false
      computeStateAtDay(state.currentDay)
      return
    }

    state.currentDay = newDay
    computeStateAtDay(newDay)

    animationFrame = requestAnimationFrame(animate)
  }

  /**
   * Start playback
   */
  function play() {
    if (!state.scenario) return
    if (state.currentDay >= state.scenario.scenario.duration) {
      state.currentDay = 0
    }
    state.isPlaying = true
    lastFrameTime = 0
    animationFrame = requestAnimationFrame(animate)
  }

  /**
   * Pause playback
   */
  function pause() {
    state.isPlaying = false
    if (animationFrame) {
      cancelAnimationFrame(animationFrame)
      animationFrame = null
    }
  }

  /**
   * Stop and reset
   */
  function stop() {
    pause()
    state.currentDay = 0
    computeStateAtDay(0)
  }

  /**
   * Seek to a specific day
   */
  function seekToDay(day: number) {
    if (!state.scenario) return
    state.currentDay = Math.max(0, Math.min(day, state.scenario.scenario.duration))
    computeStateAtDay(state.currentDay)
  }

  /**
   * Set playback speed
   */
  function setSpeed(speed: number) {
    state.playbackSpeed = speed
  }

  /**
   * Get sorted events
   */
  const sortedEvents = computed(() => {
    if (!state.scenario) return []
    return [...state.scenario.events].sort((a, b) => a.day - b.day)
  })

  /**
   * Get active remediations (from current and past events)
   */
  const activeRemediations = computed(() => {
    if (!state.scenario) return []
    const remediations: Array<{ event: SimulationEvent; remediation: any }> = []

    for (const event of state.scenario.events) {
      if (event.day <= state.currentDay) {
        for (const rem of event.remediations) {
          remediations.push({ event, remediation: rem })
        }
      }
    }

    return remediations
  })

  // API methods

  /**
   * Generate a scenario from a prompt
   */
  async function generateScenario(prompt: string): Promise<SimulateResponse> {
    const response = await $fetch<SimulateResponse>(
      `${baseUrl}/agents/simulate/${systemSlug.value}/`,
      {
        method: 'POST',
        body: { prompt },
      }
    )
    return response
  }

  /**
   * Send a chat message
   */
  async function sendChatMessage(messages: ChatMessage[]): Promise<ChatResponse> {
    const response = await $fetch<ChatResponse>(
      `${baseUrl}/agents/chat/${systemSlug.value}/`,
      {
        method: 'POST',
        body: {
          messages: messages.map(m => ({
            role: m.role,
            content: m.content,
          })),
        },
      }
    )
    return response
  }

  /**
   * Fetch saved scenarios for this system
   */
  async function fetchScenarios(): Promise<SavedScenario[]> {
    const response = await $fetch<SavedScenario[]>(
      `${baseUrl}/systems/${systemSlug.value}/scenarios/`
    )
    return response
  }

  /**
   * Fetch a specific scenario
   */
  async function fetchScenario(id: string): Promise<SavedScenario> {
    const response = await $fetch<SavedScenario>(
      `${baseUrl}/systems/${systemSlug.value}/scenarios/${id}/`
    )
    return response
  }

  /**
   * Save a scenario
   */
  async function saveScenario(
    name: string,
    description: string,
    dsl_content: SimulationScenario
  ): Promise<SavedScenario> {
    const response = await $fetch<SavedScenario>(
      `${baseUrl}/systems/${systemSlug.value}/scenarios/`,
      {
        method: 'POST',
        body: { name, description, dsl_content },
      }
    )
    return response
  }

  /**
   * Delete a scenario
   */
  async function deleteScenario(id: string): Promise<void> {
    await $fetch(`${baseUrl}/systems/${systemSlug.value}/scenarios/${id}/`, {
      method: 'DELETE',
    })
  }

  // Cleanup on unmount
  onUnmounted(() => {
    if (animationFrame) {
      cancelAnimationFrame(animationFrame)
    }
  })

  return {
    // State
    state: readonly(state),
    sortedEvents,
    activeRemediations,

    // Scenario management
    loadScenario,
    clearScenario,

    // Playback controls
    play,
    pause,
    stop,
    seekToDay,
    setSpeed,

    // State queries
    getActorQuality,
    isActorActive,
    getRelationshipQuality,

    // API
    generateScenario,
    sendChatMessage,
    fetchScenarios,
    fetchScenario,
    saveScenario,
    deleteScenario,
  }
}
