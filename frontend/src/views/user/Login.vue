<template>
  <div class="login-page">
    <!-- 登录表单区域 -->
    <div class="login-section">
      <div class="login-container">
        <div class="login-card">
          <div class="login-header">
            <h2 class="login-title">欢迎回来</h2>
            <p class="login-subtitle">登录你的 CodeForKids 账号</p>
          </div>
          <el-form :model="form" :rules="rules" ref="loginForm" class="login-form">
            <el-form-item prop="username">
              <el-input
                v-model="form.username"
                placeholder="用户名"
                prefix-icon="User"
                size="large"
                class="login-input"
              ></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="密码"
                prefix-icon="Lock"
                show-password
                size="large"
                class="login-input"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                @click="handleLogin"
                :loading="loading"
                class="login-button"
                size="large"
              >
                <span v-if="!loading">登录</span>
                <span v-else>登录中...</span>
              </el-button>
            </el-form-item>
          </el-form>
          <div class="login-footer">
            <p>还没有账号？<router-link to="/user/register" class="register-link">立即注册</router-link></p>
          </div>
        </div>
        <div class="login-illustration">
          <div class="illustration-content">
            <h3>开始你的编程之旅</h3>
            <p>与我们一起探索编程的奇妙世界，让学习变得更有趣！</p>
            <div class="feature-points">
              <div class="feature-point">
                <el-icon><Star /></el-icon>
                <span>趣味互动学习</span>
              </div>
              <div class="feature-point">
                <el-icon><Trophy /></el-icon>
                <span>进度实时追踪</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 导入Vue相关依赖
import { ref } from 'vue'
// 导入路由相关
import { useRouter } from 'vue-router'
// 导入Element Plus组件
import { ElMessage } from 'element-plus'
// 导入Element Plus图标
import { Star, Trophy } from '@element-plus/icons-vue'
// 导入用户状态管理
import { useUserStore } from '@/stores/user'

// 定义表单数据
const form = ref({
  username: '', // 用户名
  password: ''  // 密码
})

// 表单验证规则
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

// 获取路由实例
const router = useRouter()
// 获取用户状态管理实例
const userStore = useUserStore()
// 加载状态
const loading = ref(false)
// 表单引用
const loginForm = ref()

// 处理登录逻辑

const handleLogin = async () => {
  if (!loginForm.value) return
  try {
    // 验证表单
    const valid = await loginForm.value.validate()
    if (!valid) return

    // 设置加载状态
    loading.value = true

    // 调用登录接口
    const user = await userStore.login(form.value.username, form.value.password)

    // 登录成功提示
    ElMessage.success('登录成功！欢迎回来！')

    // 跳转到首页
    router.push('/')

    return user
  } catch (error) {
    // 错误处理
    if (error instanceof Error) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('登录失败，请稍后重试')
    }
    throw error
  } finally {
    // 重置加载状态
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  width: 100%;
  min-height: calc(100vh - 144px);
}

/* 登录区域 - 全宽度背景 */
.login-section {
  width: 100%;
  background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
  padding: 80px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 144px);
}

.login-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  background: white;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  min-height: 600px;
}

.login-card {
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
  line-height: 1.2;
}

.login-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.login-input {
  border-radius: 12px;
}

.login-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.login-input :deep(.el-input__wrapper:hover) {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.login-input :deep(.el-input__wrapper.is-focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.login-button {
  width: 100%;
  height: 56px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.login-footer {
  text-align: center;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
}

.login-footer p {
  color: #64748b;
  margin: 0;
  font-size: 1rem;
}

.register-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.register-link:hover {
  color: #764ba2;
}

.login-illustration {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  overflow: hidden;
  border-radius: 24px;
}

.login-illustration::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(-20px, -20px) rotate(0deg); }
  50% { transform: translate(20px, 20px) rotate(180deg); }
}

.illustration-content {
  text-align: center;
  position: relative;
  z-index: 1;
}

.illustration-content h3 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.illustration-content p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 40px;
  line-height: 1.6;
}

.feature-points {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-point {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1rem;
  opacity: 0.9;
}

.feature-point .el-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .login-container {
    grid-template-columns: 1fr;
    gap: 0;
    max-width: 500px;
  }
  .login-illustration {
    display: none;
  }
  .login-title {
    font-size: 2.2rem;
  }
}

@media (max-width: 768px) {
  .login-container {
    margin: 0 16px;
    max-width: 400px;
  }
  .login-card {
    padding: 40px 30px;
  }
  .login-title {
    font-size: 2rem;
  }
  .login-section {
    padding: 60px 0;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
  .login-title {
    font-size: 1.8rem;
  }
}
</style>
