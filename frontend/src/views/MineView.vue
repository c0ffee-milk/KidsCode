<template>
  <div class="mine-container">
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
      <h3>我的学习进度</h3>
      <el-progress :percentage="progress" :stroke-width="20" />
      <div class="badges">
        <h4>获得的徽章</h4>
        <div class="badge-list">
          <el-tag v-for="badge in badges" :key="badge" type="success">{{ badge }}</el-tag>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const username = ref(userStore.username || '小码农');
const userAvatar = ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png');
const progress = ref(45);
const badges = ref(['入门小天才', '逻辑小达人', '创意小能手']);
</script>

<style scoped>
.mine-container {
  max-width: 800px;
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
