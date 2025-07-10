<template>
  <div class="login-container">
    <div class="login-content">
      <h2 class="login-title">设置新密码</h2>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <input type="tel" placeholder="请输入手机号" v-model="phone">
        </div>
        <div class="form-group">
          <input type="text" placeholder="请输入验证码" v-model="smsCode">
          <button class="get-code-btn" :disabled="countdown > 0" @click="sendSMSCode">
            {{ countdown > 0 ? countdown + '秒后重发' : '获取验证码' }}
          </button>
        </div>
        <div class="form-group">
          <input type="password" placeholder="请输入新密码" v-model="newPassword">
        </div>
        <div class="form-group">
          <input type="password" placeholder="请确认新密码" v-model="confirmPassword">
        </div>
        <button type="submit" class="submit-btn">确认</button>
      </form>
    </div>

    <div class="floating-elements">
      <div class="floating-element element-1"></div>
      <div class="floating-element element-2"></div>
      <div class="floating-element element-3"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { authService } from '@/services/auth';
import { useRouter } from 'vue-router';

const phone = ref('');
const smsCode = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const countdown = ref(0);
const errorMessage = ref('');

const router = useRouter();

async function handleSubmit(): Promise<void> {
  try {
    if (newPassword.value !== confirmPassword.value) {
      errorMessage.value = '两次输入的密码不一致';
      return;
    }

    await authService.setPasswordWithSMS(phone.value, smsCode.value, newPassword.value);
    router.push('/login');
  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || '设置密码失败';
  }
}

async function sendSMSCode(): Promise<void> {
  if (countdown.value > 0) return;

  try {
    await authService.sendSMSCode(phone.value);
    countdown.value = 60;
    const timer = setInterval(() => {
      countdown.value--;
      if (countdown.value <= 0) clearInterval(timer);
    }, 1000);
  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || '发送验证码失败';
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
  animation: gradientBG 15s ease infinite;
  background-size: 400% 400%;
  position: relative;
  overflow: hidden;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-content {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 90%;
  z-index: 1;
  transform: translateY(0);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.login-title {
  font-size: 2.2rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-weight: 600;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.login-type-switch {
  display: flex;
  margin-bottom: 25px;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.login-type-switch button {
  flex: 1;
  padding: 12px;
  border: none;
  background: #fff;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.login-type-switch button.active {
  background: linear-gradient(90deg, #3498db, #2ecc71);
  color: #fff;
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.form-group input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px 0 0 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.get-code-btn {
  padding: 12px 15px;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  color: #fff;
  border: none;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.get-code-btn:hover {
  transform: none;
  box-shadow: none;
  opacity: 0.9;
}

.submit-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 500;
  margin-top: 10px;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(46, 204, 113, 0.4);
}

.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
}

.floating-element {
  position: absolute;
  background: rgba(100, 200, 255, 0.6);
  border-radius: 50%;
  filter: blur(20px);
}

.element-1 {
  width: 120px;
  height: 120px;
  top: 20%;
  left: 10%;
  animation: floatElement 8s ease-in-out infinite;
}

.element-2 {
  width: 100px;
  height: 100px;
  bottom: 15%;
  right: 10%;
  background: rgba(255, 200, 100, 0.6);
  animation: floatElement 10s ease-in-out infinite 2s;
}

.element-3 {
  width: 80px;
  height: 80px;
  top: 60%;
  right: 20%;
  background: rgba(100, 255, 200, 0.6);
  animation: floatElement 12s ease-in-out infinite 4s;
}

@keyframes floatElement {
  0%, 100% { transform: translate(0, 0); }
  25% { transform: translate(15px, 20px); }
  50% { transform: translate(-10px, 25px); }
  75% { transform: translate(20px, -15px); }
}
</style>

