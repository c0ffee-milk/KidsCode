<template>
  <div class="profile-container">
    <h1>用户画像</h1>
    
    <!-- 用户基本信息 -->
    <div class="user-basic-info">
      <h2>{{ userInfo.nickname }}</h2>
      <p>年龄: {{ userInfo.age }}</p>
      <p>学习时长: {{ userInfo.studyHours }}小时</p>
    </div>
    
    <!-- 课程完成进度 -->
    <div class="progress-chart">
      <h3>课程完成进度</h3>
      <div class="progress-bar">
        <div class="progress" :style="{ width: progressPercentage + '%' }"></div>
      </div>
      <p>{{ completedCourses }} / {{ totalCourses }} 课程</p>
    </div>
    
    <!-- 能力雷达图 -->
    <div class="ability-radar">
      <h3>能力评估</h3>
      <div ref="radarChart" style="width: 400px; height: 300px;"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';

const userInfo = ref({
  nickname: '编程小能手',
  age: 10,
  studyHours: 120
});

const completedCourses = ref(15);
const totalCourses = ref(20);
const progressPercentage = ref((completedCourses.value / totalCourses.value) * 100);

const radarChart = ref<HTMLElement | null>(null);

onMounted(() => {
  if (radarChart.value) {
    const chart = echarts.init(radarChart.value);
    const option = {
      tooltip: { trigger: 'item' },
      radar: {
        indicator: [
          { name: '逻辑思维', max: 100 },
          { name: '创造力', max: 100 },
          { name: '问题解决', max: 100 },
          { name: '代码规范', max: 100 },
          { name: '空间想象', max: 100 }
        ]
      },
      series: [{
        type: 'radar',
        data: [{ value: [85, 72, 68, 90, 76], name: '能力评估' }]
      }]
    };
    chart.setOption(option);
  }
});
</script>

<style scoped>
.profile-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.user-basic-info {
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.progress-chart {
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.progress-bar {
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  margin: 10px 0;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  border-radius: 10px;
  transition: width 0.5s ease;
}

.ability-radar {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}
</style>
