<template>
  <div class="competition-page">
    <!-- 固定头部区域 -->
    <div class="competition-header">
      <div class="header-content">
        <h1>
          <el-icon style="vertical-align: middle; color: #fbbf24; font-size: 32px;">
            <Trophy />
          </el-icon>
          编程竞赛广场
        </h1>
        <p class="competition-desc">参与竞赛，挑战自我，赢取荣誉与奖励！</p>
      </div>
      
      <!-- 筛选和搜索区 -->
      <div class="filter-section">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索竞赛..." 
          prefix-icon="Search"
          clearable
          class="search-input"
        />
        <el-select v-model="filterType" placeholder="全部类型" class="filter-select">
          <el-option label="🎨 全部类型" value="" />
          <el-option label="🎯 Scratch" value="Scratch" />
          <el-option label="🐍 Python" value="Python" />
          <el-option label="🌐 Web" value="Web" />
          <el-option label="🎮 游戏开发" value="Game" />
        </el-select>
        <el-select v-model="filterStatus" placeholder="竞赛状态" class="filter-select">
          <el-option label="📅 全部状态" value="" />
          <el-option label="🔥 进行中" value="ongoing" />
          <el-option label="⏰ 即将开始" value="upcoming" />
          <el-option label="✅ 已结束" value="ended" />
        </el-select>
      </div>
    </div>

    <div class="header-spacer"></div>


    <!-- 主要内容区域 -->
    <div class="content-wrapper">
      <!-- 竞赛列表 -->
      <div class="competitions-section">
        <div class="competitions-grid">
          <el-empty v-if="filteredCompetitions.length === 0" description="暂无符合条件的竞赛" />
          <el-card
            v-for="comp in filteredCompetitions"
            :key="comp.id"
            class="competition-card"
            shadow="hover"
            :body-style="{ padding: '0' }"
          >
            <!-- 竞赛状态标签 -->
            <div class="status-badge" :class="comp.status">
              {{ getStatusText(comp.status) }}
            </div>
            
            <div class="competition-cover">
              <img :src="comp.cover" :alt="comp.title" />
              <!-- 参赛人数显示 -->
              <div class="participants-badge">
                <el-icon><User /></el-icon>
                {{ comp.participants }}人参赛
              </div>
            </div>
            
            <div class="competition-info">
              <h3 class="competition-title">{{ comp.title }}</h3>
              <div class="competition-meta">
                <span>📅 {{ comp.date }}</span>
                <span>🏷️ {{ comp.type }}</span>
                <span>🎁 {{ comp.reward }}</span>
              </div>
              <div class="competition-progress" v-if="comp.status === 'ongoing'">
                <el-progress 
                  :percentage="comp.progress" 
                  :stroke-width="6"
                  :show-text="false"
                />
                <span class="progress-text">进度 {{ comp.progress }}%</span>
              </div>
              <div class="competition-actions">
                <el-button
                  type="primary"
                  size="small"
                  @click="viewDetail(comp)"
                >
                  <el-icon><View /></el-icon>
                  查看详情
                </el-button>
                <el-button
                  v-if="comp.status !== 'ended'"
                  :type="comp.joined ? 'info' : 'success'"
                  size="small"
                  :disabled="comp.joined && comp.status === 'upcoming'"
                  @click="toggleJoin(comp)"
                >
                  <el-icon>
                    <component :is="comp.joined ? 'Check' : 'Plus'" />
                  </el-icon>
                  {{ getJoinButtonText(comp) }}
                </el-button>
                <el-button
                  v-if="comp.status === 'ended' && comp.joined"
                  type="warning"
                  size="small"
                  @click="viewResults(comp)"
                >
                  <el-icon><Medal /></el-icon>
                  查看结果
                </el-button>
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
            <el-tag type="info">{{ selectedCompetition.type }}</el-tag>
            <el-tag type="warning">{{ selectedCompetition.difficulty }}</el-tag>
          </div>
          
          <p class="detail-desc">{{ selectedCompetition.description }}</p>
          
          <div class="detail-info-grid">
            <div class="info-item">
              <strong>📅 竞赛时间：</strong>
              <span>{{ selectedCompetition.date }}</span>
            </div>
            <div class="info-item">
              <strong>👥 参赛人数：</strong>
              <span>{{ selectedCompetition.participants }}人</span>
            </div>
            <div class="info-item">
              <strong>🎁 竞赛奖励：</strong>
              <span>{{ selectedCompetition.reward }}</span>
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
            v-if="selectedCompetition.status !== 'ended'"
            :type="selectedCompetition.joined ? 'info' : 'success'"
            @click="toggleJoin(selectedCompetition)"
          >
            {{ getJoinButtonText(selectedCompetition) }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 竞赛结果弹窗 -->
    <el-dialog v-model="resultsDialogVisible" title="竞赛结果" width="600px">
      <div class="results-content">
        <div class="my-result">
          <h3>我的成绩</h3>
          <div class="result-card">
            <div class="rank-info">
              <span class="rank-number">第 {{ selectedResult?.rank }} 名</span>
              <span class="score">得分: {{ selectedResult?.score }}</span>
            </div>
            <el-tag v-if="selectedResult?.award" type="success" size="large">
              🏆 {{ selectedResult.award }}
            </el-tag>
          </div>
        </div>
        
        <div class="top-results">
          <h3>排行榜前三名</h3>
          <div class="podium">
            <div v-for="(result, index) in selectedResult?.topThree" :key="index" class="podium-item">
              <div class="medal">{{ ['🥇', '🥈', '🥉'][index] }}</div>
              <div class="winner-name">{{ result.name }}</div>
              <div class="winner-score">{{ result.score }}分</div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Trophy, User, Star, View, Plus, Check, Medal } from '@element-plus/icons-vue'

interface Competition {
  id: number
  title: string
  cover: string
  description: string
  date: string
  type: string
  reward: string
  joined: boolean
  status: 'upcoming' | 'ongoing' | 'ended'
  participants: number
  progress: number
  difficulty: string
  rules: string
}

interface CompetitionResult {
  rank: number
  score: number
  award?: string
  topThree: Array<{
    name: string
    score: number
  }>
}

// 搜索和筛选
const searchQuery = ref('')
const filterType = ref('')
const filterStatus = ref('')

// 弹窗控制
const detailDialogVisible = ref(false)
const resultsDialogVisible = ref(false)
const selectedCompetition = ref<Competition | null>(null)
const selectedResult = ref<CompetitionResult | null>(null)

// 竞赛数据
const competitions = ref<Competition[]>([
  {
    id: 1,
    title: '全国少儿Scratch编程挑战赛',
    cover: 'https://placeholder.pics/svg/400x200/ffe7c2/555555/Scratch竞赛',
    description: '面向全国青少年的Scratch编程大赛，锻炼创意与逻辑思维，丰厚奖品等你来拿！参赛者需要在规定时间内完成一个完整的Scratch项目，主题为"未来世界"。',
    date: '2025-08-01 ~ 2025-08-15',
    type: 'Scratch',
    reward: '证书+奖品+积分',
    joined: false,
    status: 'upcoming',
    participants: 1234,
    progress: 0,
    difficulty: '初级',
    rules: '个人参赛，提交原创Scratch作品，主题不限，评审标准包括创意性、技术性、完整性等。'
  },
  {
    id: 2,
    title: 'Python趣味编程赛',
    cover: 'https://placeholder.pics/svg/400x200/e0f7fa/555555/Python竞赛',
    description: '用Python解决趣味编程题目，提升编程能力，赢取荣誉！包含算法题、数据处理、小游戏开发等多个环节。',
    date: '2025-07-10 ~ 2025-07-20',
    type: 'Python',
    reward: '奖牌+积分+证书',
    joined: true,
    status: 'ongoing',
    participants: 856,
    progress: 65,
    difficulty: '中级',
    rules: '团队或个人参赛，完成5道编程题目，时间限制3小时，可使用任何Python库。'
  },
  {
    id: 3,
    title: '网页创意设计赛',
    cover: 'https://placeholder.pics/svg/400x200/e7ffe0/555555/Web竞赛',
    description: '发挥你的网页设计创意，制作炫酷网页，展示你的才华！要求响应式设计，兼容多种设备。',
    date: '2025-06-05 ~ 2025-06-18',
    type: 'Web',
    reward: '荣誉证书+积分+实习机会',
    joined: true,
    status: 'ended',
    participants: 642,
    progress: 100,
    difficulty: '高级',
    rules: '个人参赛，使用HTML/CSS/JavaScript创建响应式网页，主题为"绿色环保"。'
  },
  {
    id: 4,
    title: '少儿AI编程创新赛',
    cover: 'https://placeholder.pics/svg/400x200/fff2e6/555555/AI编程',
    description: '探索人工智能的奥秘，用编程实现AI应用，培养未来科技人才！',
    date: '2025-09-15 ~ 2025-09-30',
    type: 'AI',
    reward: '奖杯+奖学金+证书',
    joined: false,
    status: 'upcoming',
    participants: 45,
    progress: 0,
    difficulty: '高级',
    rules: '团队参赛（2-3人），使用Python开发AI应用，可选择机器学习、计算机视觉或自然语言处理方向。'
  }
])

// 计算属性
const filteredCompetitions = computed(() => {
  return competitions.value.filter(comp => {
    const matchesSearch = !searchQuery.value || 
      comp.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      comp.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesType = !filterType.value || comp.type === filterType.value
    const matchesStatus = !filterStatus.value || comp.status === filterStatus.value
    
    return matchesSearch && matchesType && matchesStatus
  })
})

const totalCompetitions = computed(() => competitions.value.length)
const myJoinedCount = computed(() => competitions.value.filter(c => c.joined).length)
const myAwardsCount = computed(() => competitions.value.filter(c => c.joined && c.status === 'ended').length)

// 方法
function viewDetail(comp: Competition) {
  selectedCompetition.value = comp
  detailDialogVisible.value = true
}

function toggleJoin(comp: Competition) {
  if (comp.status === 'ended') return
  
  if (comp.joined) {
    comp.joined = false
    comp.participants--
    ElMessage.info('已取消报名')
  } else {
    comp.joined = true
    comp.participants++
    ElMessage.success('报名成功，祝你取得好成绩！')
  }
  
  // 更新选中的竞赛状态
  if (selectedCompetition.value && selectedCompetition.value.id === comp.id) {
    selectedCompetition.value.joined = comp.joined
    selectedCompetition.value.participants = comp.participants
  }
}

function viewResults(comp: Competition) {
  // 模拟结果数据
  selectedResult.value = {
    rank: Math.floor(Math.random() * 20) + 1,
    score: Math.floor(Math.random() * 40) + 60,
    award: Math.random() > 0.7 ? '优秀奖' : undefined,
    topThree: [
      { name: '编程小达人', score: 98 },
      { name: '代码小王子', score: 95 },
      { name: '算法小天才', score: 92 }
    ]
  }
  resultsDialogVisible.value = true
}

function getStatusText(status: string) {
  const statusMap = {
    'upcoming': '即将开始',
    'ongoing': '进行中',
    'ended': '已结束'
  }
  return statusMap[status as keyof typeof statusMap] || '未知'
}

function getStatusColor(status: string) {
  const colorMap = {
    'upcoming': 'info',
    'ongoing': 'success',
    'ended': 'warning'
  }
  return colorMap[status as keyof typeof colorMap] || 'default'
}

function getJoinButtonText(comp: Competition) {
  if (comp.status === 'ended') return '已结束'
  if (comp.joined) {
    return comp.status === 'upcoming' ? '已报名' : '取消参赛'
  }
  return comp.status === 'upcoming' ? '报名参赛' : '立即参赛'
}
</script>

<style scoped>
/* 页面主容器 - 关键：使用 flex 布局 */
.competition-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: rgba(255,255,255,0.96);
  padding-top: 80px; /* 只避开导航栏高度 */
}

/* 固定头部区域 */
.competition-header {
  position: sticky;
  top: 80px; /* 导航栏高度 */
  z-index: 100;
  background: rgba(255,255,255,0.98);
  backdrop-filter: blur(12px);
  border-bottom: 2px solid #ffe7c2;
  box-shadow: 0 4px 20px rgba(251,191,36,0.15);
  margin-bottom: 0;
  padding: 20px 24px 16px 24px;
}

.header-content {
  text-align: center;
  margin-bottom: 20px;
}

.competition-header h1 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #f59e42;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', '幼圆', cursive;
}

.competition-desc {
  color: #64748b;
  font-size: 1.1rem;
  margin: 0;
}

.filter-section {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  align-items: center;
  max-width: 800px;
  margin: 0 auto;
}

.search-input {
  width: 280px;
  max-width: 100%;
}

.filter-select {
  width: 150px;
}

/*过渡区 */
.header-spacer{
  height: 30px; 
  width: 100%;
}


/* 主要内容区域 - 关键：flex-grow 确保占满剩余空间 */
.content-wrapper {
  flex-grow: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 24px 32px 24px;
  width: 100%;
  box-sizing: border-box;
  margin-top: 0px;
  padding-top: 20px;
}

/* 统计卡片区域 */
.stats-section {
  margin-bottom: 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.stat-card {
  background: linear-gradient(135deg, #fffbe9 0%, #fef6e4 100%);
  border: 2px solid #ffe7c2;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(251,191,36,0.15);
}

.stat-icon {
  font-size: 2.2rem;
  color: #f59e42;
}

.stat-info h3 {
  margin: 0;
  font-size: 1.8rem;
  color: #f59e42;
  font-weight: bold;
  font-family: 'Comic Sans MS', '幼圆', cursive;
}

.stat-info p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 0.9rem;
}

/* 竞赛列表区域 */
.competitions-section {
  flex-grow: 1;
}

.competitions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 28px;
  min-height: 200px; /* 确保至少有一定高度 */
}

.competition-card {
  border-radius: 18px;
  overflow: hidden;
  background: #fffbe9;
  border: 2px solid #ffe7c2;
  box-shadow: 0 4px 16px rgba(251,191,36,0.08);
  transition: transform 0.3s cubic-bezier(.34,1.56,.64,1);
  position: relative;
  height: fit-content;
}

.competition-card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 8px 32px rgba(251,191,36,0.18);
}

.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 5;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

.status-badge.upcoming {
  background: #3b82f6;
}

.status-badge.ongoing {
  background: #10b981;
}

.status-badge.ended {
  background: #f59e0b;
}

.competition-cover {
  height: 160px;
  overflow: hidden;
  background: #f0f9ff;
  position: relative;
}

.competition-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-bottom: 2px solid #ffe7c2;
}

.participants-badge {
  position: absolute;
  bottom: 8px;
  left: 8px;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  gap: 4px;
}

.competition-info {
  padding: 18px 16px 16px 16px;
}

.competition-title {
  margin: 0 0 12px;
  font-size: 1.1rem;
  color: #f59e42;
  font-family: 'Comic Sans MS', '幼圆', cursive;
  font-weight: 600;
}

.competition-meta {
  font-size: 0.85rem;
  color: #64748b;
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.competition-progress {
  margin-bottom: 12px;
}

.progress-text {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 4px;
  display: block;
}

.competition-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* 弹窗样式 */
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
  border: 2px solid #ffe7c2;
}

.detail-content {
  flex: 1;
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
  color: #f59e42;
}

.results-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.my-result h3, .top-results h3 {
  color: #f59e42;
  margin-bottom: 16px;
}

.result-card {
  background: linear-gradient(135deg, #fffbe9 0%, #fef6e4 100%);
  border: 2px solid #ffe7c2;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.rank-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.rank-number {
  font-size: 1.2rem;
  font-weight: bold;
  color: #f59e42;
}

.score {
  font-size: 1.2rem;
  font-weight: bold;
  color: #10b981;
}

.podium {
  display: flex;
  justify-content: space-around;
  gap: 16px;
}

.podium-item {
  text-align: center;
  flex: 1;
}

.medal {
  font-size: 2rem;
  margin-bottom: 8px;
}

.winner-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.winner-score {
  color: #64748b;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .competition-page {
    padding-top: 70px;
  }
  
  .competition-header {
    top: 70px;
    padding: 16px 16px 12px 16px;
  }
  
  .competition-header h1 {
    font-size: 1.6rem;
  }
  
  .filter-section {
    flex-direction: column;
    gap: 12px;
  }
  
  .search-input, .filter-select {
    width: 100%;
  }
  
  .content-wrapper {
    padding: 16px 16px 24px 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .competitions-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .podium {
    flex-direction: column;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .stat-card {
    padding: 16px;
  }
  
  .stat-icon {
    font-size: 1.8rem;
  }
  
  .stat-info h3 {
    font-size: 1.5rem;
  }
}
</style>