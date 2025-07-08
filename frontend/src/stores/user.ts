import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login } from '../services/auth/login'
import { register } from '../services/auth/register'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const username = ref('')

  const loginUser = async (name: string, password: string) => {
    const data = await login(name, password)
    token.value = data.token
    username.value = data.name
  }

  const registerUser = async (username: string, password: string) => {
    await register(username, password)
  }

  return { token, username, login: loginUser, register: registerUser }
})
