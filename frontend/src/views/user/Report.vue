<template>
  <div class="profile-container">

    <!-- 用户基本信息 -->
    <div class="user-basic-info">
      <div class="user-header">
        <h2>{{ userInfo.name }}</h2>
        <div class="user-stats">
          <span>年龄: {{ userInfo.age }}</span>
          <span>学习时长: {{ userInfo.studyHours }}小时</span>
        </div>
      </div>
    </div>

    <!-- 热力图 -->
    <div class="heatmap-container">
      <h3>学习热力图</h3>
      <div class="heatmap-content">
        <div class="heatmap-wrapper">
          <div class="heatmap-header">
            <span class="heatmap-title">最近30天学习记录</span>
            <div class="heatmap-legend">
              <span>少</span>
              <div class="legend-colors">
                <div class="legend-item" v-for="(color, index) in legendColors" :key="index" :style="{ backgroundColor: color }"></div>
              </div>
              <span>多</span>
            </div>
          </div>
          <div class="heatmap-grid">
            <div 
              v-for="(day, index) in heatmapData" 
              :key="index"
              class="heatmap-day"
              :class="getHeatmapClass(day.count)"
              :style="{ backgroundColor: getHeatmapColor(day.count) }"
              :title="`${day.date}: ${day.count} 题`"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 课程完成进度 -->
    <div class="progress-chart">
      <h3>课程完成进度</h3>
      <div class="progress-bar">
        <div class="progress" :style="{ width: progressPercentage + '%' }"></div>
      </div>
      <p>{{ completedCourses }} / {{ totalCourses }} 课程</p>
    </div>

    <!-- 能力雷达图和评价 -->
    <div class="ability-container">
      <div class="ability-radar">
        <h3>能力评估</h3>
        <div ref="radarChart" style="width: 400px; height: 300px;"></div>
      </div>

      <div class="ability-evaluation">
        <h3>整体评价与学习建议</h3>
        <p>{{ evaluationText }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import * as echarts from 'echarts';
import { aiService } from '@/services/ai';
import { authService } from '@/services/auth';

const userInfo = ref({
  name: '编程小能手',
  age: 10,
  studyHours: 120
});

const completedCourses = ref(15);
const totalCourses = ref(20);
const progressPercentage = ref((completedCourses.value / totalCourses.value) * 100);

const radarChart = ref<HTMLElement | null>(null);
const evaluationText = ref('正在加载评估数据...');
const abilityScores = ref([0, 0, 0, 0, 0]); // 默认分数
const isLoading = ref(true);

// 加载用户信息
const loadUserInfo = async () => {
  try {
    const userData = await authService.getSelfInfo();
    userInfo.value.name = userData.name;
  } catch (error) {
    console.error('加载用户信息失败:', error);
  }
};

// 加载AI评估数据
const loadAIEvaluation = async () => {
  try {
    isLoading.value = true;
    const response = await aiService.aiEvaluate();
    
    if (response.respond && response.respond.score) {
      const scores = response.respond.score;
      abilityScores.value = [
        scores.逻辑思维,
        scores.创造力,
        scores.问题解决,
        scores.代码规范,
        scores.空间想象
      ];
      evaluationText.value = response.respond.comment;
    }
  } catch (error: any) {
    console.error('加载AI评估失败:', error);
    // ElMessage.error('加载评估数据失败，请稍后重试');
    // 使用默认数据
    abilityScores.value = [85, 72, 68, 90, 76];
    evaluationText.value = '该学员在代码规范方面表现优秀，逻辑思维和空间想象能力较强，创造力和问题解决能力有待进一步提升。';
  } finally {
    isLoading.value = false;
  }
};

// 初始化雷达图
const initRadarChart = () => {
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
        data: [{ value: abilityScores.value, name: '能力评估' }]
      }]
    };
    chart.setOption(option);
    
    // 监听窗口大小变化，重新调整图表大小
    window.addEventListener('resize', () => {
      chart.resize();
    });
  }
};

// 热力图相关数据和方法
const legendColors = ref(['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']);

// 生成最近30天的学习数据
const generateHeatmapData = () => {
  const data = [];
  const today = new Date();
  
  for (let i = 29; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    
    // 模拟数据：随机生成0-10的题目数量
    const count = Math.floor(Math.random() * 11);
    
    data.push({
      date: date.toISOString().split('T')[0],
      count: count
    });
  }
  
  return data;
};

const heatmapData = ref(generateHeatmapData());

// 生命周期钩子
onMounted(async () => {
  try {
    // 并行加载用户信息和AI评估数据
    await Promise.all([
      loadUserInfo(),
      loadAIEvaluation()
    ]);
    
    // 初始化雷达图
    initRadarChart();
  } catch (error) {
    console.error('页面初始化失败:', error);
  }
});

// 根据题目数量获取颜色
const getHeatmapColor = (count: number) => {
  if (count === 0) return '#ebedf0';
  if (count <= 2) return '#9be9a8';
  if (count <= 4) return '#40c463';
  if (count <= 6) return '#30a14e';
  return '#216e39';
};

// 根据题目数量获取CSS类名
const getHeatmapClass = (count: number) => {
  if (count === 0) return 'heatmap-empty';
  if (count <= 2) return 'heatmap-low';
  if (count <= 4) return 'heatmap-medium';
  if (count <= 6) return 'heatmap-high';
  return 'heatmap-very-high';
};
</script>

<style scoped>
.profile-container {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

h2, h3 {
  font-weight: 600;
  color: #333;
}

p {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
}

.user-basic-info h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.ability-evaluation p {
  font-size: 15px;
  line-height: 1.8;
}

.profile-container {
  padding-top: 200px;
  max-width: 800px;
  margin: 0 auto;
}

.user-basic-info {
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-stats {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #666;
}

.heatmap-container {
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.heatmap-container h3 {
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}

.heatmap-content {
  min-height: 200px;
  background: white;
  border-radius: 4px;
  padding: 15px;
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

.ability-container {
  display: flex;
  gap: 20px;
}

.ability-evaluation {
  flex: 1;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

/* 热力图样式 */
.heatmap-wrapper {
  width: 100%;
}

.heatmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.heatmap-title {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.heatmap-legend {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #666;
}

.legend-colors {
  display: flex;
  gap: 2px;
}

.legend-item {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 6px;
  width: 100%;
  padding: 15px;
}

.heatmap-day {
  width: 100%;
  height: 35px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  min-width: 0;
}

.heatmap-day:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 10;
}

.heatmap-empty {
  background-color: #ebedf0;
}

.heatmap-low {
  background-color: #9be9a8;
}

.heatmap-medium {
  background-color: #40c463;
}

.heatmap-high {
  background-color: #30a14e;
}

.heatmap-very-high {
  background-color: #216e39;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .heatmap-grid {
    grid-template-columns: repeat(8, 1fr);
    grid-template-rows: repeat(4, 1fr);
    gap: 4px;
    padding: 10px;
  }
  
  .heatmap-day {
    height: 25px;
  }
  
  .heatmap-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
