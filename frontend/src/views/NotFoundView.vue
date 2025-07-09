<template>
  <div class="not-found-container">
    <div class="error-content">
      <div class="error-illustration">
        <img 
          src="https://img.freepik.com/free-vector/404-error-with-landscape-concept-illustration_114360-7898.jpg" 
          alt="404插图" 
          class="illustration"
          style="width: 300px; height: auto; border-radius: 16px;"
        />
        <div class="floating-elements">
          <div class="floating-element element-1"></div>
          <div class="floating-element element-2"></div>
          <div class="floating-element element-3"></div>
        </div>
      </div>

      <h1 class="error-title">404 - 页面迷路了</h1>
      <p class="error-message">
        <el-icon class="error-icon"><WarnTriangleFilled /></el-icon>
        <span>小探险家，你发现了一个未知领域</span>
      </p>

      <el-button
        type="primary"
        size="large"
        @click="$router.push('/')"
        class="home-button"
        round
      >
        <el-icon><HomeFilled /></el-icon>
        <span>返回安全基地</span>
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
  animation: gradientBG 15s ease infinite;
  background-size: 400% 400%;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.error-content {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 90%;
  transform: translateY(0);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.error-illustration {
  position: relative;
  margin-bottom: 2rem;
}

.illustration {
  width: 200px;
  height: auto;
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.1));
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
  width: 100px;
  height: 100px;
  top: -30px;
  left: 20px;
  animation: floatElement 8s ease-in-out infinite;
}

.element-2 {
  width: 80px;
  height: 80px;
  bottom: -20px;
  right: 10px;
  background: rgba(255, 200, 100, 0.6);
  animation: floatElement 10s ease-in-out infinite 2s;
}

.element-3 {
  width: 60px;
  height: 60px;
  top: 50%;
  right: 30px;
  background: rgba(100, 255, 200, 0.6);
  animation: floatElement 12s ease-in-out infinite 4s;
}

@keyframes floatElement {
  0%, 100% { transform: translate(0, 0); }
  25% { transform: translate(10px, 15px); }
  50% { transform: translate(-5px, 20px); }
  75% { transform: translate(15px, -10px); }
}

.error-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  font-weight: 600;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.error-icon {
  font-size: 1.5rem;
  color: #f39c12;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.home-button {
  margin-top: 1.5rem;
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.home-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(46, 204, 113, 0.4);
}
</style>
