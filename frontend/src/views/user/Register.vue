<template>
  <div class="register-page">
    <div class="register-section">
      <div class="register-container">
        <div class="register-card">
          <div class="register-header">
            <h2 class="register-title">加入我们</h2>
            <p class="register-subtitle">创建你的 CodeForKids 账号，开始编程之旅</p>
          </div>
          <el-form :model="form" :rules="rules" ref="registerForm" class="register-form">
            <el-form-item prop="username">
              <el-input
                v-model="form.username"
                placeholder="用户名"
                prefix-icon="User"
                size="large"
                class="register-input"
              ></el-input>
            </el-form-item>
            <el-form-item prop="phone">
              <el-input
                v-model="form.phone"
                placeholder="手机号"
                prefix-icon="Iphone"
                size="large"
                class="register-input"
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
                class="register-input"
              ></el-input>
            </el-form-item>
            <el-form-item prop="confirmPassword">
              <el-input
                v-model="form.confirmPassword"
                type="password"
                placeholder="确认密码"
                prefix-icon="Lock"
                show-password
                size="large"
                class="register-input"
              ></el-input>
            </el-form-item>
            <el-form-item prop="code">
              <div class="code-input-container">
                <el-input
                  v-model="form.code"
                  placeholder="验证码"
                  prefix-icon="Message"
                  size="large"
                  class="register-input code-input"
                ></el-input>
                <el-button
                  type="primary"
                  size="large"
                  class="send-code-btn register-input "
                  @click="sendCode"
                  :disabled="isSending"
                >
                  {{ isSending ? `${countdown}秒后重试` : '获取验证码' }}
                </el-button>
              </div>
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                @click="handleRegister"
                :loading="loading"
                class="register-button"
                size="large"
              >
                <span v-if="!loading">注册</span>
                <span v-else>注册中...</span>
              </el-button>
            </el-form-item>
          </el-form>
          <div class="register-footer">
            <p>已有账号？<router-link to="/user/login" class="login-link">立即登录</router-link></p>
          </div>
        </div>
        <div class="register-illustration">
          <div class="illustration-content">
            <h3>加入编程大家庭</h3>
            <p>成为我们的一员，与全世界的小朋友一起学习编程！</p>
            <div class="feature-points">
              <div class="feature-point">
                <el-icon><Star /></el-icon>
                <span>创意编程项目</span>
              </div>
              <div class="feature-point">
                <el-icon><Medal /></el-icon>
                <span>学习成就徽章</span>
              </div>
              <div class="feature-point">
                <el-icon><Connection /></el-icon>
                <span>社区互动交流</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star, Medal, Connection, Iphone, Message } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const form = ref({
  username: '',
  phone: '',
  password: '',
  confirmPassword: '',
  code: ''
})

const validatePass = (rule: any, value: string, callback: Function) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.value.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 16, message: '长度在 3 到 16 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass, trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ]
}

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const isSending = ref(false)
const countdown = ref(60)
const registerForm = ref()

const sendCode = async () => {
  if (!form.value.phone) {
    ElMessage.error('请输入手机号')
    return
  }

  try {
    isSending.value = true
    await userStore.sendCode(form.value.phone)
    ElMessage.success('验证码已发送')

    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
        isSending.value = false
        countdown.value = 60
      }
    }, 1000)
  } catch (error) {
    isSending.value = false
    if (error instanceof Error) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('发送验证码失败')
    }
  }
}

const handleRegister = async () => {
  if (!registerForm.value) return
  try {
    const valid = await registerForm.value.validate()
    if (!valid) return
    loading.value = true
    await userStore.register(form.value.username, form.value.phone, form.value.password, form.value.code)
    ElMessage.success('注册成功！欢迎加入CodeForKids！')
    router.push('/user/login')
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  width: 100%;
  min-height: calc(100vh - 144px);
}

/* 注册区域 - 全宽度背景 */
.register-section {
  width: 100%;
  background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
  padding: 80px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 144px);
}

.register-container {
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

.register-card {
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.register-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
  line-height: 1.2;
}

.register-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.register-input {
  border-radius: 12px;
}

.register-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.register-input :deep(.el-input__wrapper:hover) {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.register-input :deep(.el-input__wrapper.is-focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.register-button {
  width: 100%;
  height: 56px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.code-input-container {
  display: flex;
  gap: 12px;
}

.code-input {
  flex: 1;
}

.send-code-btn {
  width: 140px;
  border-radius: 12px;
  background: linear-gradient(135deg, #38b2ac 0%, #4fd1c7 100%);
  border: none;
}

.send-code-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(56, 178, 172, 0.3);
}

.register-footer {
  text-align: center;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
}

.register-footer p {
  color: #64748b;
  margin: 0;
  font-size: 1rem;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.login-link:hover {
  color: #764ba2;
}

.register-illustration {
  background: linear-gradient(135deg, #38b2ac 0%, #4fd1c7 100%);
  padding: 60px 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  overflow: hidden;
  border-radius: 24px;
}

.register-illustration::before {
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
  .register-container {
    grid-template-columns: 1fr;
    gap: 0;
    max-width: 500px;
  }
  .register-illustration {
    display: none;
  }
  .register-title {
    font-size: 2.2rem;
  }
}

@media (max-width: 768px) {
  .register-container {
    margin: 0 16px;
    max-width: 400px;
  }
  .register-card {
    padding: 40px 30px;
  }
  .register-title {
    font-size: 2rem;
  }
  .register-section {
    padding: 60px 0;
  }
}

@media (max-width: 480px) {
  .register-card {
    padding: 30px 20px;
  }
  .register-title {
    font-size: 1.8rem;
  }
}
</style>
