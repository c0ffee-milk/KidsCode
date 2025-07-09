import axios from 'axios'

// 登录响应接口
interface LoginResponse {
  user: {
    id: number       // 用户ID
    phone: string    // 手机号
    name: string     // 用户名
  }
  token: string      // 认证令牌
}

// API基础URL，优先使用环境变量配置
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api'

// 认证服务
export const authService = {
  // 使用短信验证码登录
  async loginWithSMS(phone: string, smsCode: string): Promise<LoginResponse> {
    const response = await axios.post<LoginResponse>(`${API_URL}/auth/sms`, { phone, smsCode })
    return response.data
  },

  // 使用密码登录
  async loginWithPassword(phone: string, password: string): Promise<LoginResponse> {
    const response = await axios.post<LoginResponse>(`${API_URL}/auth/password`, { phone, password })
    return response.data
  },

  // 发送短信验证码
  async sendSMSCode(phone: string): Promise<{ success: boolean }> {
    const response = await axios.post<{ success: boolean }>(`${API_URL}/auth/send-sms`, { phone })
    return response.data
  }
}
