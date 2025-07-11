import axios from 'axios'

// 登录响应接口
interface LoginResponse {
  user: {
    id: number       // 用户ID
    phone: string    // 手机号
    name: string     // 用户名
  }
  token: string      // 认证令牌
  refresh_token: string      // 刷新令牌
}

// API基础URL，优先使用环境变量配置
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// 认证服务
export const authService = {
  // 使用短信验证码登录
  async loginWithSMS(phone: string, smsCode: string): Promise<LoginResponse> {
    console.log('请求参数:', { phone, code: smsCode }) // 打印请求参数

    try {
      const response = await axios.post<LoginResponse>(`${API_URL}/auth/login_with_code`,{ phone, code: smsCode })
      console.log('响应数据:', response.data) // 打印响应数据
      return response.data
    } catch (error: any) {
      console.error('请求失败:', error.response?.data || error.message) // 打印错误信息
      throw error
    }
  },

  // 使用密码登录
  async loginWithPassword(phone: string, password: string): Promise<LoginResponse> {
    const response = await axios.post<LoginResponse>(`${API_URL}/auth/login_with_password`, { phone, password })
    console.log('响应数据:', response.data) // 打印响应数据
    return response.data
  },

  // 发送短信验证码
  async sendSMSCode(phone: string): Promise<{ success: boolean }> {
    const response = await axios.post<{ success: boolean }>(`${API_URL}/auth/send-code`, { phone })
    console.log('响应数据:', response.data) // 打印响应数据
    return response.data
  },

  // 使用短信验证码设置密码
  async setPasswordWithSMS(phone: string, smsCode: string, newPassword: string): Promise<{ success: boolean }> {
    console.log('请求参数:', { phone, code: smsCode, password: newPassword }) // 打印请求参数

    const response = await axios.post<{ success: boolean }>(`${API_URL}/auth/update-info`, {
      phone,
      code: smsCode,
      password: newPassword
    })
    console.log('响应数据:', response.data) // 打印响应数据
    return response.data
  },

  // 更新用户信息
  async updateUserInfo(phone: string, name: string, code: string, password?: string): Promise<{ success: boolean }> {
    console.log('请求参数:', { phone, name, code, password });

    const response = await axios.post<{ success: boolean }>(`${API_URL}/auth/update-info`, {
      phone,
      name,
      code,
      ...(password && { password })
    });

    console.log('响应数据:', response.data);
    return response.data;
  },

  // 获取当前用户信息
  async getSelfInfo(): Promise<{ phone: string; name: string }> {
    console.log('Token type:', typeof localStorage.getItem('token'));
    console.log('Token value:', localStorage.getItem('token'));
    const response = await axios.post<{
        status: string;
        message: string;
        name: string;
        phone: string
    }>(`${API_URL}/auth/self_info`, {}, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });

    return {
        phone: response.data.phone,
        name: response.data.name
    };
}}
