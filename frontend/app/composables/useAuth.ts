/**
 * Authentication composable for managing JWT tokens and user state
 */

interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  full_name: string
  title: string
  country: string
  department: string
  job_title: string
  role: 'superadmin' | 'r4s_manager' | 'project_staff'
  role_display: string
  is_active: boolean
  created_at: string
  updated_at: string
  last_login: string | null
}

interface AuthTokens {
  access: string
  refresh: string
}

interface LoginResponse extends AuthTokens {
  user: User
}

export function useAuth() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBase

  const user = useState<User | null>('auth-user', () => null)
  const accessToken = useState<string | null>('auth-access-token', () => null)
  const refreshToken = useState<string | null>('auth-refresh-token', () => null)

  // Initialize from localStorage on client side
  if (import.meta.client) {
    const storedAccess = localStorage.getItem('access_token')
    const storedRefresh = localStorage.getItem('refresh_token')
    const storedUser = localStorage.getItem('user')

    if (storedAccess && storedRefresh) {
      accessToken.value = storedAccess
      refreshToken.value = storedRefresh
      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser)
        } catch {
          // Invalid JSON, clear storage
          localStorage.removeItem('user')
        }
      }
    }
  }

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isSuperadmin = computed(() => user.value?.role === 'superadmin')
  const isR4SManager = computed(() => user.value?.role === 'r4s_manager')
  const isProjectStaff = computed(() => user.value?.role === 'project_staff')

  async function login(email: string, password: string): Promise<{ success: boolean; error?: string }> {
    try {
      const response = await $fetch<LoginResponse>(`${baseUrl}/auth/login/`, {
        method: 'POST',
        body: { email, password },
      })

      accessToken.value = response.access
      refreshToken.value = response.refresh
      user.value = response.user

      // Store in localStorage
      if (import.meta.client) {
        localStorage.setItem('access_token', response.access)
        localStorage.setItem('refresh_token', response.refresh)
        localStorage.setItem('user', JSON.stringify(response.user))
      }

      return { success: true }
    } catch (error: any) {
      const message = error?.data?.detail || 'Login failed. Please check your credentials.'
      return { success: false, error: message }
    }
  }

  async function refreshAccessToken(): Promise<boolean> {
    if (!refreshToken.value) return false

    try {
      const response = await $fetch<{ access: string }>(`${baseUrl}/auth/refresh/`, {
        method: 'POST',
        body: { refresh: refreshToken.value },
      })

      accessToken.value = response.access

      if (import.meta.client) {
        localStorage.setItem('access_token', response.access)
      }

      return true
    } catch {
      // Refresh token expired, logout
      logout()
      return false
    }
  }

  function logout() {
    accessToken.value = null
    refreshToken.value = null
    user.value = null

    if (import.meta.client) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    }

    navigateTo('/login')
  }

  async function fetchCurrentUser(): Promise<User | null> {
    if (!accessToken.value) return null

    try {
      const response = await $fetch<User>(`${baseUrl}/users/me/`, {
        headers: {
          Authorization: `Bearer ${accessToken.value}`,
        },
      })

      user.value = response

      if (import.meta.client) {
        localStorage.setItem('user', JSON.stringify(response))
      }

      return response
    } catch {
      // Token might be expired, try to refresh
      const refreshed = await refreshAccessToken()
      if (refreshed) {
        return fetchCurrentUser()
      }
      return null
    }
  }

  async function updateProfile(data: Partial<User>): Promise<{ success: boolean; error?: string }> {
    if (!accessToken.value) return { success: false, error: 'Not authenticated' }

    try {
      const response = await $fetch<User>(`${baseUrl}/users/me/`, {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${accessToken.value}`,
        },
        body: data,
      })

      user.value = response

      if (import.meta.client) {
        localStorage.setItem('user', JSON.stringify(response))
      }

      return { success: true }
    } catch (error: any) {
      return { success: false, error: error?.data?.detail || 'Failed to update profile' }
    }
  }

  async function changePassword(oldPassword: string, newPassword: string, confirmPassword: string): Promise<{ success: boolean; error?: string }> {
    if (!accessToken.value) return { success: false, error: 'Not authenticated' }

    try {
      await $fetch(`${baseUrl}/users/change_password/`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken.value}`,
        },
        body: {
          old_password: oldPassword,
          new_password: newPassword,
          new_password_confirm: confirmPassword,
        },
      })

      return { success: true }
    } catch (error: any) {
      const errors = error?.data
      const message = errors?.old_password?.[0] || errors?.new_password?.[0] || errors?.new_password_confirm?.[0] || 'Failed to change password'
      return { success: false, error: message }
    }
  }

  // Utility function for making authenticated API calls
  function authFetch<T>(url: string, options: any = {}): Promise<T> {
    return $fetch<T>(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${accessToken.value}`,
      },
    })
  }

  return {
    user,
    accessToken,
    isAuthenticated,
    isSuperadmin,
    isR4SManager,
    isProjectStaff,
    login,
    logout,
    refreshAccessToken,
    fetchCurrentUser,
    updateProfile,
    changePassword,
    authFetch,
  }
}

export type { User, AuthTokens, LoginResponse }
