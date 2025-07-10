import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface User {
  id: number
  phone: string
  name: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token') || null)
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token') || null)

  function setUser(userData: User): void {
    user.value = userData
  }

  function setTokens(newToken: string, newRefreshToken: string): void {
    token.value = newToken
    refreshToken.value = newRefreshToken
    localStorage.setItem('token', newToken)
    localStorage.setItem('refresh_token', newRefreshToken)
  }

  function clear(): void {
    user.value = null
    token.value = null
    refreshToken.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
  }

  return { user, token, refreshToken, setUser, setTokens, clear }
})
