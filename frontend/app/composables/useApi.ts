/**
 * API composable for interacting with the Django REST backend
 */

interface System {
  id: string
  slug: string
  name: string
  description: string
  region: string
  country: string
  sector: string
  sector_display: string
  subsector: string
  assessment_date: string | null
  version: string
  actor_count: number
  risk_count: number
  updated_at: string
}

interface Actor {
  id: string
  slug: string
  name: string
  actor_type: string
  actor_type_display: string
  position_x: number | null
  position_y: number | null
}

interface Risk {
  id: string
  slug: string
  name: string
  description: string
  category: string
  category_display: string
  likelihood: string
  likelihood_display: string
}

interface Relationship {
  id: string
  from_actor: string
  from_actor_name: string
  to_actor: string
  to_actor_name: string
  relationship_type: string
  goods_services: string
  quality: string
  quality_display: string
}

export function useApi() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBase

  async function fetchSystems(params?: { sector?: string; country?: string }) {
    const query = new URLSearchParams()
    if (params?.sector) query.append('sector', params.sector)
    if (params?.country) query.append('country', params.country)

    const queryString = query.toString()
    const url = `${baseUrl}/systems/${queryString ? `?${queryString}` : ''}`

    return useFetch<{ results: System[] }>(url, {
      key: `systems-${queryString}`,
    })
  }

  async function fetchSystem(slug: string) {
    return useFetch<System>(`${baseUrl}/systems/${slug}/`)
  }

  async function fetchSystemExport(slug: string) {
    return useFetch<{ dsl: string }>(`${baseUrl}/systems/${slug}/export/`)
  }

  async function fetchActors(systemSlug?: string) {
    const url = systemSlug
      ? `${baseUrl}/actors/?system=${systemSlug}`
      : `${baseUrl}/actors/`

    return useFetch<{ results: Actor[] }>(url)
  }

  async function fetchRisks(systemSlug?: string) {
    const url = systemSlug
      ? `${baseUrl}/risks/?system=${systemSlug}`
      : `${baseUrl}/risks/`

    return useFetch<{ results: Risk[] }>(url)
  }

  async function fetchRelationships(systemSlug?: string) {
    const url = systemSlug
      ? `${baseUrl}/relationships/?system=${systemSlug}`
      : `${baseUrl}/relationships/`

    return useFetch<{ results: Relationship[] }>(url)
  }

  return {
    fetchSystems,
    fetchSystem,
    fetchSystemExport,
    fetchActors,
    fetchRisks,
    fetchRelationships,
  }
}

export type { System, Actor, Risk, Relationship }
