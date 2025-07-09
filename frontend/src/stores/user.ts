import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login } from '../services/auth/login'
import { register } from '../services/auth/register'
import { sendCode } from '../services/auth/register'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const refreshToken = ref('')
  const username = ref('')
  const userId = ref('')

  const loginUser = async (username: string, password: string) => {
    const data = await login(username, password)
    token.value = data.token
    refreshToken.value = data.refresh_token
    // 这里的 username 变量名与参数名冲突，导致报错，修改为使用 ref 定义的 username
    username.value = data.user_name
    userId.value = data.id
  }

  const registerUser = async (username: string, phone: string, password: string, code: string) => {
    const data = await register(username, phone, password, code)
    token.value = data.token
    refreshToken.value = data.refresh_token
    username.value = data.user_name
    userId.value = data.id
  }

  const sendVerificationCode = async (phone: string) => {
    await sendCode(phone)
  }

  const logout = () => {
    token.value = ''
    refreshToken.value = ''
    username.value = ''
    userId.value = ''
  }

  return {
    token,
    refreshToken,
    username,
    userId,
    login: loginUser,
    register: registerUser,
    sendCode: sendVerificationCode,
    logout
  }
})
