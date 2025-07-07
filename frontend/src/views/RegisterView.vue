<template>
  <div class="register-container">
    <el-form :model="form" :rules="rules" ref="registerForm">
      <el-form-item prop="username">
        <el-input v-model="form.username" placeholder="用户名"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input v-model="form.password" type="password" placeholder="密码"></el-input>
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码"></el-input>
      </el-form-item>
      <el-button type="primary" @click="handleRegister">注册</el-button>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
})

const validatePass = (rule: any, value: string, callback: Function) => {
  if (value !== form.value.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass, trigger: 'blur' },
  ],
}

const router = useRouter()
const handleRegister = () => {
  // 这里添加实际注册逻辑
  ElMessage.success('注册成功')
  router.push('/login')
}
</script>
