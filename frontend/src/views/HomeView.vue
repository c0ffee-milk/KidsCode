<template>
  <div class="home-page">
    <!-- Hero 区域 -->
    <div class="hero-section">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">欢迎来到少儿编程世界</h1>
          <p class="hero-subtitle">通过有趣的游戏学习编程基础</p>
          <div class="action-buttons">
            <el-button type="primary" size="large" @click="navigateTo('/learn')">
              <el-icon><Edit /></el-icon>
              开始学习
            </el-button>
            <el-button size="large" @click="navigateTo('/register')">
              <el-icon><UserFilled /></el-icon>
              注册账号
            </el-button>
          </div>
        </div>
        <div class="hero-illustration">
          <div class="code-blocks">
            <div class="code-block">console.log("Hello World!");</div>
            <div class="code-block">for(let i=0; i&lt;5; i++) {...}</div>
            <div class="code-block">function greet(name) {...}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features 区域 -->
    <div class="features-section">
      <div class="features-container">
        <div class="section-header">
          <h2>为什么选择我们?</h2>
          <p>专为少儿打造的编程学习平台，让编程变得简单有趣</p>
        </div>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.title">
            <div class="feature-icon">
              <el-icon :size="48">
                <component :is="feature.icon" />
              </el-icon>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats 区域 -->
    <div class="stats-section">
      <div class="stats-container">
        <div class="stats-grid">
          <div class="stat-item" v-for="stat in stats" :key="stat.label">
            <div class="stat-number">{{ stat.number }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA 区域 -->
    <div class="cta-section">
      <div class="cta-container">
        <div class="cta-content">
          <h2>准备好开始你的编程之旅了吗？</h2>
          <p>加入我们，让孩子在快乐中学习编程！</p>
          <el-button type="primary" size="large" @click="router.push('/learn')">
            立即开始
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { Edit, UserFilled, MagicStick, Connection, DataBoard } from '@element-plus/icons-vue';

const router = useRouter();


const features = [
  {
    title: '趣味学习',
    description: '通过游戏和动画学习编程概念，让孩子在玩耍中掌握编程技能',
    icon: MagicStick
  },
  {
    title: '实时反馈',
    description: '即时看到代码运行结果，帮助孩子理解程序执行过程',
    icon: Connection
  },
  {
    title: '进度追踪',
    description: '详细记录学习进度和成就，激励孩子持续学习',
    icon: DataBoard
  }
];

const stats = [
  { number: '1000+', label: '学习用户' },
  { number: '50+', label: '编程练习' },
  { number: '95%', label: '完成率' },
  { number: '4.9', label: '用户评分' }
];
</script>

<style scoped>
.home-page {
  width: 100%;
  min-height: calc(100vh - 144px);
}

/* Hero 区域 - 全宽度背景 */
.hero-section {
  width: 100%;
  background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
  padding: 80px 0;
}

.hero-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 24px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.4rem;
  color: #64748b;
  margin-bottom: 40px;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.action-buttons .el-button {
  padding: 16px 32px;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
}

.hero-illustration {
  display: flex;
  justify-content: center;
  align-items: center;
}

.code-blocks {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.code-block {
  background: #1e293b;
  color: #e2e8f0;
  padding: 16px 20px;
  border-radius: 12px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 14px;
  box-shadow: 0 4px 20px rgba(30, 41, 59, 0.3);
  animation: float 3s ease-in-out infinite;
}

.code-block:nth-child(2) {
  animation-delay: -1s;
}

.code-block:nth-child(3) {
  animation-delay: -2s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

/* Features 区域 */
.features-section {
  width: 100%;
  background: white;
  padding: 80px 0;
}

.features-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 16px;
}

.section-header p {
  font-size: 1.2rem;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 40px;
}

.feature-card {
  background: white;
  padding: 40px 32px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  color: white;
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 16px;
}

.feature-card p {
  color: #64748b;
  line-height: 1.6;
  font-size: 1rem;
}

/* Stats 区域 - 全宽度彩色背景 */
.stats-section {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 0;
}

.stats-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
}

.stat-item {
  text-align: center;
  color: white;
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* CTA 区域 */
.cta-section {
  width: 100%;
  background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
  padding: 80px 0;
}

.cta-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.cta-content {
  text-align: center;
}

.cta-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 16px;
}

.cta-content p {
  font-size: 1.2rem;
  color: #64748b;
  margin-bottom: 32px;
}

.cta-content .el-button {
  padding: 16px 48px;
  border-radius: 50px;
  font-size: 18px;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }

  .hero-title {
    font-size: 2.8rem;
  }
}

@media (max-width: 768px) {
  .hero-container,
  .features-container,
  .stats-container,
  .cta-container {
    padding: 0 16px;
  }

  .hero-title {
    font-size: 2.2rem;
  }

  .action-buttons {
    justify-content: center;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }

  .hero-section,
  .features-section,
  .stats-section,
  .cta-section {
    padding: 60px 0;
  }
}
</style>
