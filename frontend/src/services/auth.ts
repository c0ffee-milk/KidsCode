import axios from 'axios'

interface LoginResponse {
  user: {
    id: number
    phone: string
    name: string
  }
  token: string
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api'

export const authService = {
  async loginWithSMS(phone: string, smsCode: string): Promise<LoginResponse> {
    const response = await axios.post<LoginResponse>(`${API_URL}/auth/sms`, { phone, smsCode })
    return response.data
  },

  async loginWithPassword(phone: string, password: string): Promise<LoginResponse> {
    const response = await axios.post<LoginResponse>(`${API_URL}/auth/password`, { phone, password })
    return response.data
  },

  async sendSMSCode(phone: string): Promise<{ success: boolean }> {
    const response = await axios.post<{ success: boolean }>(`${API_URL}/auth/send-sms`, { phone })
    return response.data
  }
}
