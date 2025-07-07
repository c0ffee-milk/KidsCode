import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',
    username: ''
  }),
  actions: {
    login(username: string, password: string) {
      // 这里添加实际登录API调用
      this.token = 'mock-token'
      this.username = username
    },
    register(username: string, password: string) {
      // 这里添加实际注册API调用
      return true
    },
    logout() {
      this.token = ''
      this.username = ''
    }
  }
})