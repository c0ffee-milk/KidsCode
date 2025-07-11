<template>
  <div class="competition-center">
    <!-- 页面头部 -->
    <div class="center-header">
      <div class="header-content">
        <h1>
          <el-icon style="vertical-align: middle; color: #fbbf24; font-size: 32px;">
            <Trophy />
          </el-icon>
          竞赛中心
        </h1>
        <p class="header-desc">展示编程才华，挑战自我极限，收获成长与荣誉！</p>
      </div>
    </div>

    <!-- 个人竞赛统计概览 -->
    <div class="stats-overview">
      <el-card class="stats-card">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">
              <el-icon><Trophy /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ userCompetitionStats.totalParticipated }}</span>
              <span class="stat-label">参与竞赛</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <el-icon><Medal /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ userCompetitionStats.totalAwards }}</span>
              <span class="stat-label">获得奖项</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <el-icon><Star /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ userCompetitionStats.bestRank }}</span>
              <span class="stat-label">最佳排名</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ userCompetitionStats.ongoingCount }}</span>
              <span class="stat-label">进行中</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧导航 -->
      <div class="sidebar">
        <el-menu
          :default-active="activeTab"
          @select="handleTabChange"
          class="center-menu"
        >
          <el-menu-item index="overview">
            <el-icon><DataBoard /></el-icon>
            <span>竞赛概览</span>
          </el-menu-item>
          <el-menu-item index="available">
            <el-icon><Plus /></el-icon>
            <span>可参加竞赛</span>
          </el-menu-item>
          <el-menu-item index="my-competitions">
            <el-icon><User /></el-icon>
            <span>我的竞赛</span>
          </el-menu-item>
          <el-menu-item index="results">
            <el-icon><Medal /></el-icon>
            <span>竞赛成绩</span>
          </el-menu-item>
          <el-menu-item index="achievements">
            <el-icon><Trophy /></el-icon>
            <span>竞赛成就</span>
          </el-menu-item>
        </el-menu>
      </div>

      <!-- 右侧内容 -->
      <div class="content-area">
        <!-- 竞赛概览 -->
        <div v-if="activeTab === 'overview'" class="tab-content">
          <el-card class="overview-card">
            <template #header>
              <span>最新竞赛动态</span>
            </template>
            <div class="competition-highlights">
              <div 
                v-for="comp in highlightCompetitions" 
                :key="comp.id" 
                class="highlight-item"
                @click="viewCompetitionDetail(comp)"
              >
                <img :src="comp.cover" :alt="comp.title" class="highlight-cover" />
                <div class="highlight-info">
                  <h4>{{ comp.title }}</h4>
                  <p>{{ comp.description }}</p>
                  <div class="highlight-meta">
                    <el-tag :type="getStatusColor(comp.status)" size="small">
                      {{ getStatusText(comp.status) }}
                    </el-tag>
                    <span class="participants">{{ comp.participants }}人参与</span>
                  </div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 竞赛日历 -->
          <el-card class="calendar-card">
            <template #header>
              <span>竞赛日历</span>
            </template>
            <div class="calendar-content">
              <el-timeline class="competition-timeline">
                <el-timeline-item
                  v-for="event in upcomingEvents"
                  :key="event.id"
                  :timestamp="event.date"
                  :type="event.type"
                >
                  <el-card class="timeline-card">
                    <h4>{{ event.title }}</h4>
                    <p>{{ event.description }}</p>
                    <el-button 
                      type="primary" 
                      size="small"
                      @click="goToCompetition(event.competitionId)"
                    >
                      查看详情
                    </el-button>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </div>
          </el-card>
        </div>

        <!-- 可参加竞赛 -->
        <div v-if="activeTab === 'available'" class="tab-content">
          <!-- 筛选器 -->
          <div class="filter-section">
            <el-input 
              v-model="searchQuery" 
              placeholder="搜索竞赛..." 
              prefix-icon="Search"
              clearable
              class="search-input"
            />
            <el-select v-model="filterType" placeholder="竞赛类型" class="filter-select">
              <el-option label="全部类型" value="" />
              <el-option label="Scratch" value="scratch" />
              <el-option label="Python" value="python" />
              <el-option label="Web" value="web" />
              <el-option label="游戏开发" value="game" />
            </el-select>
            <el-select v-model="filterDifficulty" placeholder="难度等级" class="filter-select">
              <el-option label="全部难度" value="" />
              <el-option label="初级" value="beginner" />
              <el-option label="中级" value="intermediate" />
              <el-option label="高级" value="advanced" />
            </el-select>
          </div>

          <!-- 竞赛列表 -->
          <div class="competitions-grid">
            <el-card
              v-for="comp in filteredAvailableCompetitions"
              :key="comp.id"
              class="competition-card"
              shadow="hover"
              @click="viewCompetitionDetail(comp)"
            >
              <div class="card-header">
                <img :src="comp.cover" :alt="comp.title" class="comp-cover" />
                <div class="status-badges">
                  <el-tag :type="getStatusColor(comp.status)" size="small">
                    {{ getStatusText(comp.status) }}
                  </el-tag>
                  <el-tag type="info" size="small">{{ comp.difficulty }}</el-tag>
                </div>
              </div>
              <div class="card-content">
                <h3>{{ comp.title }}</h3>
                <p>{{ comp.description }}</p>
                <div class="comp-meta">
                  <span>🗓️ {{ comp.registrationDeadline }}</span>
                  <span>🏷️ {{ getCategoryName(comp.category) }}</span>
                  <span>👥 {{ comp.participants }}人</span>
                </div>
                <div class="card-actions">
                  <el-button 
                    type="primary" 
                    size="small"
                    @click.stop="registerCompetition(comp)"
                    :disabled="comp.registered || isRegistrationClosed(comp)"
                  >
                    {{ comp.registered ? '已报名' : '立即报名' }}
                  </el-button>
                  <el-button 
                    type="info" 
                    size="small"
                    @click.stop="viewCompetitionDetail(comp)"
                  >
                    查看详情
                  </el-button>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- 我的竞赛 -->
        <div v-if="activeTab === 'my-competitions'" class="tab-content">
          <el-tabs v-model="myCompetitionsTab" type="card">
            <el-tab-pane label="进行中" name="ongoing">
              <div class="my-competitions-list">
                <el-card
                  v-for="comp in myOngoingCompetitions"
                  :key="comp.id"
                  class="my-competition-card"
                >
                  <div class="my-comp-header">
                    <h3>{{ comp.title }}</h3>
                    <el-tag type="success">进行中</el-tag>
                  </div>
                  <div class="my-comp-progress">
                    <span>竞赛进度</span>
                    <el-progress 
                      :percentage="comp.progress" 
                      :stroke-width="6"
                    />
                  </div>
                  <div class="my-comp-actions">
                    <el-button type="primary" @click="continueCompetition(comp)">
                      继续竞赛
                    </el-button>
                    <el-button type="info" @click="viewCompetitionDetail(comp)">
                      查看详情
                    </el-button>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="已完成" name="completed">
              <div class="my-competitions-list">
                <el-card
                  v-for="comp in myCompletedCompetitions"
                  :key="comp.id"
                  class="my-competition-card"
                >
                  <div class="my-comp-header">
                    <h3>{{ comp.title }}</h3>
                    <el-tag type="warning">已完成</el-tag>
                  </div>
                  <div class="my-comp-result">
                    <div class="result-item">
                      <span>最终排名</span>
                      <strong>第 {{ comp.finalRank }} 名</strong>
                    </div>
                    <div class="result-item">
                      <span>得分</span>
                      <strong>{{ comp.finalScore }} 分</strong>
                    </div>
                    <div class="result-item" v-if="comp.award">
                      <span>获得奖项</span>
                      <el-tag type="success">{{ comp.award }}</el-tag>
                    </div>
                  </div>
                  <div class="my-comp-actions">
                    <el-button type="info" @click="viewResults(comp)">
                      查看成绩
                    </el-button>
                    <el-button type="primary" @click="viewCompetitionDetail(comp)">
                      竞赛详情
                    </el-button>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <!-- 竞赛成绩 -->
        <div v-if="activeTab === 'results'" class="tab-content">
          <el-card class="results-overview">
            <template #header>
              <span>成绩统计</span>
            </template>
            <div class="results-stats">
              <div class="result-chart">
                <!-- 这里可以添加图表组件 -->
                <div class="chart-placeholder">
                  <el-icon><TrendCharts /></el-icon>
                  <p>成绩趋势图</p>
                </div>
              </div>
              <div class="result-summary">
                <div class="summary-item">
                  <span>平均分数</span>
                  <strong>{{ userCompetitionStats.averageScore }}</strong>
                </div>
                <div class="summary-item">
                  <span>最高分数</span>
                  <strong>{{ userCompetitionStats.highestScore }}</strong>
                </div>
                <div class="summary-item">
                  <span>获奖率</span>
                  <strong>{{ userCompetitionStats.awardRate }}%</strong>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 详细成绩列表 -->
          <el-card class="results-list">
            <template #header>
              <span>历史成绩</span>
            </template>
            <el-table :data="competitionResults" style="width: 100%">
              <el-table-column prop="competitionTitle" label="竞赛名称" />
              <el-table-column prop="date" label="参赛时间" width="120" />
              <el-table-column prop="score" label="得分" width="80" />
              <el-table-column prop="rank" label="排名" width="80" />
              <el-table-column prop="participants" label="参赛人数" width="100" />
              <el-table-column label="奖项" width="120">
                <template #default="scope">
                  <el-tag v-if="scope.row.award" type="success" size="small">
                    {{ scope.row.award }}
                  </el-tag>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="100">
                <template #default="scope">
                  <el-button 
                    type="text" 
                    size="small"
                    @click="viewDetailedResult(scope.row)"
                  >
                    查看详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>

        <!-- 竞赛成就 -->
        <div v-if="activeTab === 'achievements'" class="tab-content">
          <el-card class="achievements-card">
            <template #header>
              <span>竞赛成就徽章</span>
            </template>
            <div class="achievements-grid">
              <div
                v-for="achievement in competitionAchievements"
                :key="achievement.id"
                :class="['achievement-item', { earned: achievement.earned }]"
                @click="showAchievementDetail(achievement)"
              >
                <div class="achievement-icon">
                  <el-icon><Medal /></el-icon>
                </div>
                <div class="achievement-info">
                  <h4>{{ achievement.name }}</h4>
                  <p>{{ achievement.description }}</p>
                  <div class="achievement-progress" v-if="!achievement.earned">
                    <el-progress 
                      :percentage="achievement.progress" 
                      :stroke-width="4"
                      :show-text="false"
                    />
                    <span class="progress-text">{{ achievement.progress }}%</span>
                  </div>
                  <span v-else class="earned-date">
                    获得于 {{ achievement.earnedDate }}
                  </span>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>

    <!-- 竞赛详情弹窗 -->
    <el-dialog 
      v-model="detailDialogVisible" 
      :title="selectedCompetition?.title" 
      width="700px"
      v-if="selectedCompetition"
    >
      <div class="competition-detail">
        <img :src="selectedCompetition.cover" class="detail-cover" />
        <div class="detail-content">
          <div class="detail-tags">
            <el-tag :type="getStatusColor(selectedCompetition.status)">
              {{ getStatusText(selectedCompetition.status) }}
            </el-tag>
            <el-tag type="info">{{ selectedCompetition.category }}</el-tag>
            <el-tag type="warning">{{ selectedCompetition.difficulty }}</el-tag>
          </div>
          
          <p class="detail-desc">{{ selectedCompetition.description }}</p>
          
          <div class="detail-info-grid">
            <div class="info-item">
              <strong>📅 竞赛时间：</strong>
              <span>{{ selectedCompetition.startDate }} ~ {{ selectedCompetition.endDate }}</span>
            </div>
            <div class="info-item">
              <strong>⏰ 报名截止：</strong>
              <span>{{ selectedCompetition.registrationDeadline }}</span>
            </div>
            <div class="info-item">
              <strong>👥 参赛人数：</strong>
              <span>{{ selectedCompetition.participants }}人</span>
            </div>
            <div class="info-item">
              <strong>🎁 竞赛奖励：</strong>
              <span>{{ selectedCompetition.rewards }}</span>
            </div>
            <div class="info-item">
              <strong>📝 竞赛规则：</strong>
              <span>{{ selectedCompetition.rules }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
          <el-button
            v-if="!selectedCompetition.registered && !isRegistrationClosed(selectedCompetition)"
            type="success"
            @click="registerCompetition(selectedCompetition)"
          >
            立即报名
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Trophy, Medal, Star, Clock, DataBoard, Plus, User,
  TrendCharts
} from '@element-plus/icons-vue'

// 接口定义
interface Competition {
  id: number
  title: string
  description: string
  cover: string
  category: string
  difficulty: string
  status: 'upcoming' | 'ongoing' | 'ended'
  startDate: string
  endDate: string
  registrationDeadline: string
  participants: number
  registered: boolean
  progress?: number
  finalRank?: number
  finalScore?: number
  award?: string
  rewards: string
  rules: string
}

interface CompetitionResult {
  id: number
  competitionTitle: string
  date: string
  score: number
  rank: number
  participants: number
  award?: string
}

interface Achievement {
  id: number
  name: string
  description: string
  earned: boolean
  progress: number
  earnedDate?: string
}

// 响应式数据
const activeTab = ref('overview')
const myCompetitionsTab = ref('ongoing')
const searchQuery = ref('')
const filterType = ref('')
const filterDifficulty = ref('')
const detailDialogVisible = ref(false)
const selectedCompetition = ref<Competition | null>(null)

// 用户竞赛统计（与个人中心保持一致）
const userCompetitionStats = ref({
  totalParticipated: 8,
  totalAwards: 3,
  bestRank: 2,
  ongoingCount: 2,
  averageScore: 85.5,
  highestScore: 96,
  awardRate: 37.5
})

// 精选竞赛
const highlightCompetitions = ref([
  {
    id: 1,
    title: '全国青少年编程挑战赛',
    description: '面向全国中小学生的编程竞赛，展示编程才华',
    cover: 'https://placeholder.pics/svg/300x150/667eea/white/全国编程赛',
    status: 'upcoming',
    participants: 1250
  },
  {
    id: 2,
    title: 'Scratch创意动画赛',
    description: '用Scratch制作创意动画，发挥想象力',
    cover: 'https://placeholder.pics/svg/300x150/10b981/white/Scratch动画',
    status: 'ongoing',
    participants: 856
  }
])

// 即将到来的竞赛事件
const upcomingEvents = ref([
  {
    id: 1,
    title: 'Python编程赛报名开始',
    description: '初级Python编程竞赛开始接受报名',
    date: '2025-02-01',
    type: 'success',
    competitionId: 3
  },
  {
    id: 2,
    title: 'Web设计赛截止报名',
    description: '网页设计创意赛即将截止报名',
    date: '2025-02-05',
    type: 'warning',
    competitionId: 4
  }
])

// 可参加的竞赛
const availableCompetitions = ref<Competition[]>([
  {
    id: 1,
    title: '全国青少年编程挑战赛',
    description: '面向全国中小学生的综合性编程竞赛，包含多个编程语言和难度等级',
    cover: 'https://placeholder.pics/svg/300x200/667eea/white/全国编程赛',
    category: 'scratch',
    difficulty: 'intermediate',
    status: 'upcoming',
    startDate: '2025-03-01',
    endDate: '2025-03-15',
    registrationDeadline: '2025-02-20',
    participants: 1250,
    registered: false,
    rewards: '冠军证书+奖金+编程学习资源',
    rules: '个人参赛，需在规定时间内完成编程任务，评审标准包括代码质量、创新性等'
  },
  {
    id: 2,
    title: 'Scratch创意动画大赛',
    description: '用Scratch制作富有创意的动画作品，展现艺术与技术的结合',
    cover: 'https://placeholder.pics/svg/300x200/10b981/white/Scratch动画',
    category: 'scratch',
    difficulty: 'beginner',
    status: 'ongoing',
    startDate: '2025-01-15',
    endDate: '2025-02-15',
    registrationDeadline: '2025-01-31',
    participants: 856,
    registered: true,
    progress: 45,
    rewards: '优秀作品展示+证书+编程套件',
    rules: '提交原创Scratch动画作品，主题自选，时长不超过3分钟'
  }
])

// 我参与的竞赛
const myOngoingCompetitions = computed(() => 
  availableCompetitions.value.filter(comp => comp.registered && comp.status === 'ongoing')
)

const myCompletedCompetitions = ref<Competition[]>([
  {
    id: 10,
    title: 'Python基础编程赛',
    description: 'Python基础语法和算法竞赛',
    cover: 'https://placeholder.pics/svg/300x200/f59e0b/white/Python竞赛',
    category: 'python',
    difficulty: 'beginner',
    status: 'ended',
    startDate: '2024-12-01',
    endDate: '2024-12-15',
    registrationDeadline: '2024-11-25',
    participants: 423,
    registered: true,
    finalRank: 15,
    finalScore: 88,
    award: '优秀奖',
    rewards: '证书+编程书籍',
    rules: '完成指定编程题目，限时3小时'
  }
])

// 竞赛成绩记录（与个人中心学习记录关联）
const competitionResults = ref<CompetitionResult[]>([
  {
    id: 1,
    competitionTitle: 'Python基础编程赛',
    date: '2024-12-15',
    score: 88,
    rank: 15,
    participants: 423,
    award: '优秀奖'
  },
  {
    id: 2,
    competitionTitle: 'Scratch动画创作赛',
    date: '2024-11-20',
    score: 92,
    rank: 8,
    participants: 356,
    award: '创意奖'
  }
])

// 竞赛成就（与个人中心徽章系统整合）
const competitionAchievements = ref<Achievement[]>([
  {
    id: 1,
    name: '初出茅庐',
    description: '参加第一场编程竞赛',
    earned: true,
    progress: 100,
    earnedDate: '2024-11-20'
  },
  {
    id: 2,
    name: '获奖达人',
    description: '在竞赛中获得3次奖项',
    earned: true,
    progress: 100,
    earnedDate: '2024-12-15'
  },
  {
    id: 3,
    name: '竞赛专家',
    description: '参加10场不同类型的竞赛',
    earned: false,
    progress: 60
  }
])

// 计算属性
const filteredAvailableCompetitions = computed(() => {
  return availableCompetitions.value.filter(comp => {
    const matchesSearch = !searchQuery.value || 
      comp.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesType = !filterType.value || comp.category === filterType.value
    const matchesDifficulty = !filterDifficulty.value || comp.difficulty === filterDifficulty.value
    
    return matchesSearch && matchesType && matchesDifficulty
  })
})

// 方法
const handleTabChange = (tab: string) => {
  activeTab.value = tab
}

const getCategoryName = (category: string) => {
  const categoryMap = {
    'scratch': 'Scratch',
    'python': 'Python',
    'web': 'Web开发',
    'game': '游戏开发'
  }
  return categoryMap[category] || category
}

const getStatusText = (status: string) => {
  const statusMap = {
    'upcoming': '即将开始',
    'ongoing': '进行中',
    'ended': '已结束'
  }
  return statusMap[status] || '未知'
}

const getStatusColor = (status: string) => {
  const colorMap = {
    'upcoming': 'info',
    'ongoing': 'success',
    'ended': 'warning'
  }
  return colorMap[status] || 'default'
}

const isRegistrationClosed = (comp: Competition) => {
  const deadline = new Date(comp.registrationDeadline)
  return new Date() > deadline
}

const viewCompetitionDetail = (comp: Competition) => {
  selectedCompetition.value = comp
  detailDialogVisible.value = true
}

const registerCompetition = async (comp: Competition) => {
  try {
    // 这里调用注册API
    comp.registered = true
    comp.participants++
    
    // 更新用户统计
    userCompetitionStats.value.totalParticipated++
    if (comp.status === 'ongoing') {
      userCompetitionStats.value.ongoingCount++
    }
    
    ElMessage.success('报名成功！祝你取得好成绩！')
    
    // 关闭弹窗
    detailDialogVisible.value = false
  } catch (error) {
    ElMessage.error('报名失败，请重试')
  }
}

const continueCompetition = (comp: Competition) => {
  // 跳转到竞赛页面继续答题
  ElMessage.info(`继续参与：${comp.title}`)
}

const viewResults = (comp: Competition) => {
  // 查看详细竞赛结果
  ElMessage.info(`查看${comp.title}的详细成绩`)
}

const viewDetailedResult = (result: CompetitionResult) => {
  // 查看单个竞赛的详细结果
  ElMessage.info(`查看${result.competitionTitle}的详细成绩`)
}

const showAchievementDetail = (achievement: Achievement) => {
  ElMessageBox.alert(achievement.description, achievement.name, {
    confirmButtonText: '确定',
    type: achievement.earned ? 'success' : 'info'
  })
}

const goToCompetition = (competitionId: number) => {
  const comp = availableCompetitions.value.find(c => c.id === competitionId)
  if (comp) {
    viewCompetitionDetail(comp)
  }
}

// 生命周期
onMounted(() => {
  // 加载竞赛数据
  loadCompetitionData()
})

const loadCompetitionData = async () => {
  try {
    // 这里可以调用API加载最新的竞赛数据
    // 确保与个人中心的数据保持同步
  } catch (error) {
    ElMessage.error('加载竞赛数据失败')
  }
}
</script>

<style scoped>
.competition-center {
  min-height: calc(100vh - 160px);
  background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
  padding: 40px 0;
  margin-top: 200px;
}

.center-header {
  text-align: center;
  margin-bottom: 40px;
}

.center-header h1 {
  font-size: 2.5rem;
  color: #fbbf24;
  margin-bottom: 12px;
  font-weight: 700;
}

.header-desc {
  color: #64748b;
  font-size: 1.1rem;
  margin: 0;
}

.stats-overview {
  max-width: 1200px;
  margin: 0 auto 40px;
  padding: 0 24px;
}

.stats-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 32px;
  padding: 20px 0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.stat-info {
  flex: 1;
}

.stat-number {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 32px;
}

.sidebar {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 20px 0;
  height: fit-content;
}

.center-menu {
  border: none;
}

.center-menu .el-menu-item {
  margin: 4px 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.center-menu .el-menu-item:hover {
  background: rgba(251, 191, 36, 0.1);
  color: #fbbf24;
}

.center-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
}

.content-area {
  min-height: 500px;
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 概览页面样式 */
.overview-card,
.calendar-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.competition-highlights {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.highlight-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.highlight-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.highlight-cover {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}

.highlight-info {
  flex: 1;
}

.highlight-info h4 {
  margin: 0 0 8px;
  color: #1e293b;
}

.highlight-info p {
  margin: 0 0 8px;
  color: #64748b;
  font-size: 0.9rem;
}

.highlight-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.participants {
  font-size: 0.8rem;
  color: #64748b;
}

/* 筛选器样式 */
.filter-section {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-input {
  width: 280px;
}

.filter-select {
  width: 150px;
}

/* 竞赛卡片样式 */
.competitions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.competition-card {
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.competition-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

.card-header {
  position: relative;
}

.comp-cover {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.status-badges {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 4px;
}

.card-content {
  padding: 16px;
}

.card-content h3 {
  margin: 0 0 8px;
  color: #1e293b;
}

.card-content p {
  margin: 0 0 12px;
  color: #64748b;
  font-size: 0.9rem;
}

.comp-meta {
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-actions {
  display: flex;
  gap: 8px;
}

/* 我的竞赛样式 */
.my-competitions-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.my-competition-card {
  border-radius: 12px;
}

.my-comp-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.my-comp-header h3 {
  margin: 0;
  color: #1e293b;
}

.my-comp-progress {
  margin-bottom: 16px;
}

.my-comp-progress span {
  display: block;
  margin-bottom: 8px;
  color: #64748b;
  font-size: 0.9rem;
}

.my-comp-result {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.result-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.result-item span {
  color: #64748b;
  font-size: 0.9rem;
}

.result-item strong {
  color: #1e293b;
  font-size: 1.1rem;
}

.my-comp-actions {
  display: flex;
  gap: 8px;
}

/* 成绩页面样式 */
.results-overview {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.results-stats {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 12px;
  color: #64748b;
}

.chart-placeholder .el-icon {
  font-size: 48px;
  margin-bottom: 8px;
}

.result-summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.summary-item strong {
  color: #fbbf24;
  font-size: 1.2rem;
}

.results-list {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* 成就页面样式 */
.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.achievement-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  transition: all 0.3s ease;
  cursor: pointer;
  opacity: 0.6;
}

.achievement-item.earned {
  border-color: #fbbf24;
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.05) 0%, rgba(245, 158, 11, 0.05) 100%);
  opacity: 1;
}

.achievement-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.achievement-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.achievement-info {
  flex: 1;
}

.achievement-info h4 {
  margin: 0 0 4px;
  color: #1e293b;
}

.achievement-info p {
  margin: 0 0 8px;
  color: #64748b;
  font-size: 0.9rem;
}

.achievement-progress {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-text {
  font-size: 0.8rem;
  color: #64748b;
}

.earned-date {
  font-size: 0.8rem;
  color: #fbbf24;
  font-weight: 500;
}

/* 详情弹窗样式 */
.competition-detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-cover {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 12px;
}

.detail-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.detail-desc {
  color: #333;
  line-height: 1.6;
  margin-bottom: 20px;
}

.detail-info-grid {
  display: grid;
  gap: 12px;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.info-item strong {
  min-width: 100px;
  color: #fbbf24;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    order: 2;
  }
  
  .center-menu {
    display: flex;
    overflow-x: auto;
  }
  
  .center-menu .el-menu-item {
    margin: 4px 8px;
    min-width: 120px;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .competitions-grid {
    grid-template-columns: 1fr;
  }
  
  .results-stats {
    grid-template-columns: 1fr;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-section {
    flex-direction: column;
  }
  
  .search-input,
  .filter-select {
    width: 100%;
  }
}
</style>