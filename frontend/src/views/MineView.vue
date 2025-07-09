<template>
  <div class="mine-page">
    <div class="mine-container">
      <div class="page-header">
        <h1 class="page-title">我的学习中心</h1>
        <p class="page-desc">查看学习进度和个人成就</p>
      </div>

      <div class="mine-content">
        <el-card class="user-card">
          <div class="user-info">
            <el-avatar :size="100" :src="userAvatar" />
            <div class="user-details">
              <h2>{{ username }}</h2>
              <p>编程小能手</p>
            </div>
          </div>
        </el-card>

        <el-card class="progress-card">
          <template #header>
            <div class="card-header">
              <el-icon><DataBoard /></el-icon>
              <span>我的学习进度</span>
            </div>
          </template>
          <div class="progress-content">
            <el-progress :percentage="progress" :stroke-width="20" />
            <p class="progress-text">已完成 {{ progress }}% 的课程</p>
          </div>
        </el-card>

        <el-card class="badges-card">
          <template #header>
            <div class="card-header">
              <el-icon><Medal /></el-icon>
              <span>获得的徽章</span>
            </div>
          </template>
          <div class="badge-list">
            <div v-for="badge in badges" :key="badge" class="badge-item">
              <el-icon><Trophy /></el-icon>
              <span>{{ badge }}</span>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { DataBoard, Medal, Trophy } from '@element-plus/icons-vue';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const username = ref(userStore.username || '小码农');
const userAvatar = ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png');
const progress = ref(45);
const badges = ref(['入门小天才', '逻辑小达人', '创意小能手']);
</script>

<style scoped>
.mine-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.user-card {
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-details h2 {
  margin: 0;
  color: #333;
}

.user-details p {
  margin: 5px 0 0;
  color: #666;
}

.progress-card {
  margin-bottom: 20px;
}

.badge-list {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
</style>
