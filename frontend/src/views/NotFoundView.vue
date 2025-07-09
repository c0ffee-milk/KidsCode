<template>
  <div class="not-found-container">
    <div class="error-content">
      <h1 class="error-title">404 - 页面未找到</h1>
      <p class="error-message">
        <el-icon class="error-icon"><WarnTriangleFilled /></el-icon>
        <span>您访问的页面不存在或已被移除</span>
      </p>
      <el-button type="primary" size="large" @click="$router.push('/')" class="home-button">
        返回首页
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  background-color: #f5f7fa;
}

.error-content {
  text-align: center;
  padding: 2rem;
}

.error-title {
  font-size: 2.5rem;
  color: #303133;
  margin-bottom: 1rem;
}

.error-description {
  font-size: 1.2rem;
  color: #606266;
  margin-bottom: 2rem;
}

.error-image {
  margin: 2rem 0;
}

.home-button {
  margin-top: 1rem;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  color: #606266;
}

.error-icon {
  font-size: 1.2rem;
  color: #e6a23c;
}
</style>
