/**
 * Types for the Risk Simulator DSL and simulation state management
 */

// Event types for disaster simulation
export type EventType =
  | 'disaster_onset'
  | 'resource_shortage'
  | 'capacity_reduction'
  | 'infrastructure_damage'
  | 'demand_surge'
  | 'intervention'
  | 'recovery'

// Priority levels for remediation actions
export type Priority = 'critical' | 'high' | 'medium' | 'low'

// Quality states for actors and relationships
export type QualityState = 'good' | 'stressed' | 'bad' | 'absent'

// Impact on an actor or relationship
export interface Impact {
  actor?: string        // Glob pattern for actors (e.g., "health-center-*")
  relationship?: string // Pattern like "source-slug -> target-slug"
  attribute: 'quality' | 'active'
  from: QualityState | boolean
  to: QualityState | boolean
}

// Suggested remediation action
export interface Remediation {
  priority: Priority
  action: string
  actor: string
}

// Single event in a simulation scenario
export interface SimulationEvent {
  day: number
  type: EventType
  name: string
  description: string
  impacts: Impact[]
  remediations: Remediation[]
}

// Scenario metadata
export interface ScenarioInfo {
  name: string
  description: string
  duration: number
}

// Complete simulation scenario (DSL structure)
export interface SimulationScenario {
  scenario: ScenarioInfo
  events: SimulationEvent[]
}

// Saved scenario from the database
export interface SavedScenario {
  id: string
  name: string
  description: string
  duration: number
  event_count: number
  created_at: string
  updated_at: string
  dsl_content?: SimulationScenario
}

// Override for an actor's state during simulation
export interface ActorOverride {
  quality?: QualityState
  active?: boolean
}

// Override for a relationship's state during simulation
export interface RelationshipOverride {
  quality?: QualityState
}

// Current state of the simulation playback
export interface SimulationState {
  scenario: SimulationScenario | null
  currentDay: number
  isPlaying: boolean
  playbackSpeed: number  // 1, 2, or 4
  actorOverrides: Map<string, ActorOverride>
  relationshipOverrides: Map<string, RelationshipOverride>
  activeEvent: SimulationEvent | null
}

// Chat message for disaster exploration
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  scenario?: SimulationScenario | null
  timestamp?: Date
}

// API response from simulate endpoint
export interface SimulateResponse {
  scenario: SimulationScenario | null
  raw_response: string
  raw_yaml?: string
  error?: string
}

// API response from chat endpoint
export interface ChatResponse {
  message: string
  scenario: SimulationScenario | null
  error?: string
}

// Event type metadata for display
export const EVENT_TYPE_INFO: Record<EventType, { icon: string; label: string; color: string }> = {
  disaster_onset: { icon: '⚠️', label: 'Disaster Onset', color: '#DC2626' },
  resource_shortage: { icon: '📦', label: 'Resource Shortage', color: '#F59E0B' },
  capacity_reduction: { icon: '👥', label: 'Capacity Reduction', color: '#F97316' },
  infrastructure_damage: { icon: '🏥', label: 'Infrastructure Damage', color: '#EF4444' },
  demand_surge: { icon: '📈', label: 'Demand Surge', color: '#8B5CF6' },
  intervention: { icon: '🛡️', label: 'Intervention', color: '#22C55E' },
  recovery: { icon: '✅', label: 'Recovery', color: '#10B981' },
}

// Priority metadata for display
export const PRIORITY_INFO: Record<Priority, { label: string; color: string; bgColor: string }> = {
  critical: { label: 'Critical', color: '#DC2626', bgColor: '#FEE2E2' },
  high: { label: 'High', color: '#F97316', bgColor: '#FFEDD5' },
  medium: { label: 'Medium', color: '#F59E0B', bgColor: '#FEF3C7' },
  low: { label: 'Low', color: '#6B7280', bgColor: '#F3F4F6' },
}
