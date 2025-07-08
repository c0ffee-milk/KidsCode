import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const username = ref('')

  const login = async (username: string, password: string) => {
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username, password })
    })

    if (!response.ok) throw new Error('登录失败')

    const data = await response.json()
    token.value = data.token
    username.value = data.username
  }

  const register = async (username: string, password: string) => {
    const response = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username, password })
    })

    if (!response.ok) throw new Error('注册失败')
  }

  return { token, username, login, register }
})
