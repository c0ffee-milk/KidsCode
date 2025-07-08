<template>
  <div class="home-container">
    <div class="hero-section">
      <h1>欢迎来到少儿编程世界</h1>
      <p class="subtitle">通过有趣的游戏学习编程基础</p>
      <div class="action-buttons">
        <el-button
          type="primary"
          size="large"
          @click="userStore.token ? $router.push('/learn') : $router.push('/login')"
        >
          {{ userStore.token ? '继续学习' : '开始学习' }}
        </el-button>
        <el-button size="large" @click="userStore.token ? userStore.logout() : $router.push('/register')">
          {{ userStore.token ? '退出登录' : '注册账号' }}
        </el-button>
      </div>
    </div>

    <div class="features-section">
      <h2>为什么选择我们?</h2>
      <div class="features-grid">
        <div class="feature-card" v-for="feature in features" :key="feature.title">
          <el-icon :size="40">
            <component :is="feature.icon" />
          </el-icon>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </div>
    </div>

    <el-backtop :right="100" :bottom="100" target=".home-container" />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { MagicStick, Connection, DataBoard, Trophy } from '@element-plus/icons-vue';

import { useUserStore } from '@/stores/user';
const userStore = useUserStore();

const router = useRouter();


const features = [
  {
    title: '趣味学习',
    description: '通过游戏和动画学习编程概念',
    icon: MagicStick
  },
  {
    title: '实时反馈',
    description: '即时看到你的代码运行结果',
    icon: Connection
  },
  {
    title: '进度追踪',
    description: '记录你的学习进度和成就',
    icon: DataBoard
  },
  {
    title: '奖励机制',
    description: '完成课程获得徽章和积分奖励',
    icon: Trophy
  }
];
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 10px;
  margin-bottom: 40px;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: #333;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 30px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.features-section {
  text-align: center;
  margin-bottom: 40px;
}

.features-section h2 {
  font-size: 2rem;
  margin-bottom: 40px;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.feature-card {
  padding: 30px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  margin: 15px 0 10px;
  color: #333;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}
</style>
<script setup lang="ts"></script>
