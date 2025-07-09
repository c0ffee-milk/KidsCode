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

  function setUser(userData: User): void {
    user.value = userData
  }

  function setToken(newToken: string): void {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function clear(): void {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  return { user, token, setUser, setToken, clear }
})
