import axios from 'axios'

// API基础URL，优先使用环境变量配置
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// AI分析响应接口
interface AIAnalysisResponse {
  message: string
  respond: {
    is_right: boolean
    analysis: string
  }
}

// AI判定响应接口
interface AIJudgeResponse {
  message: string
  respond: {
    movement: string
    is_right: boolean
  }
}

// AI评估响应接口
interface AIEvaluateResponse {
  message: string
  respond: {
    score: {
      逻辑思维: number
      创造力: number
      问题解决: number
      代码规范: number
      空间想象: number
    }
    comment: string
  }
}

// AI服务
export const aiService = {
  // 获取AI分析
  async getAnalysis(subject: string, content: string): Promise<AIAnalysisResponse> {
    try {
      const response = await axios.post<AIAnalysisResponse>(`${API_URL}/ai/ai_analyze`, {
        subject,
        content
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      return response.data
    } catch (error: any) {
      console.error('AI分析请求失败:', error.response?.data || error.message)
      throw error
    }
  },

  // AI判定
  async aiJudge(subject: string, content: string): Promise<AIJudgeResponse> {
    try {
      const response = await axios.post<AIJudgeResponse>(`${API_URL}/ai/ai_judge`, {
        subject,
        content
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      return response.data
    } catch (error: any) {
      console.error('AI判定请求失败:', error.response?.data || error.message)
      throw error
    }
  },

  // AI评估
  async aiEvaluate(): Promise<AIEvaluateResponse> {
    try {
      const response = await axios.post<AIEvaluateResponse>(`${API_URL}/ai/ai_evaluate`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      return response.data
    } catch (error: any) {
      console.error('AI评估请求失败:', error.response?.data || error.message)
      throw error
    }
  }
} 