<template>
  <div class="share-page">
    <!-- 1. 页面标题区 -->
    <div class="page-header">
      <h1>
        <el-icon style="vertical-align: middle; color: #fbbf24; font-size: 32px;">
          <StarFilled />
        </el-icon>
        作品分享乐园
      </h1>
      <el-button type="success" size="large" @click="showPublishDialog" class="publish-btn">
        <el-icon><Star /></el-icon>
        发布作品
      </el-button>
    </div>
    
    <!-- 筛选区和温馨提示区 -->
    <div class="filter-sticky">
      <div class="filter-container">
        <!-- 2. 筛选区 -->
        <div class="filter-section">
          <el-input 
            v-model="searchQuery" 
            placeholder="搜索你喜欢的作品吧~" 
            prefix-icon="Search"
            clearable
            class="search-input"
          />
          <el-select v-model="filterCategory" placeholder="全部分类" class="filter-select">
            <el-option label="全部分类" value="" />
            <el-option label="Scratch" value="scratch" />
            <el-option label="Python" value="python" />
            <el-option label="Web" value="web" />
            <el-option label="游戏" value="game" />
          </el-select>
        </div>
        <!-- 3. 温馨提示区 -->
        <div class="tips-banner">
          <el-icon style="color: #fbbf24; font-size: 22px; margin-right: 6px;"><StarFilled /></el-icon>
          <span>欢迎来到作品分享乐园！你可以浏览、点赞、评论同学们的作品，也可以发布自己的创意项目哦！</span>
        </div>
      </div>
    </div>

    <!-- 4. 作品展示区 -->
    <div class="works-grid">
      <el-empty v-if="pagedWorks.length === 0" description="还没有作品，快来发布你的第一个作品吧！" />
      <el-card 
        v-for="work in pagedWorks" 
        :key="work.id" 
        class="work-card"
        shadow="hover"
        :body-style="{ padding: '0' }"
      >
        <div class="work-cover" @click="viewWorkDetail(work)">
          <img :src="work.cover" :alt="work.title" loading="lazy">
          <div class="cover-badge" v-if="work.category">
            <el-tag :type="getCategoryColor(work.category)" size="small" effect="dark">
              {{ getCategoryName(work.category) }}
            </el-tag>
          </div>
        </div>
        <div class="work-info">
          <h3 class="work-title" @click="viewWorkDetail(work)">
            {{ work.title }}
            <el-icon v-if="work.likes >= 30" style="color: #fbbf24; margin-left: 4px;"><StarFilled /></el-icon>
          </h3>
          <p class="work-author">
            <el-icon style="color: #60a5fa;"><UserFilled /></el-icon>
            {{ work.author }}
          </p>
          <div class="work-meta">
            <span class="work-date">{{ work.createTime }}</span>
          </div>
          <div class="work-actions">
            <el-button
              size="small"
              @click.stop="likeWork(work)"
              :icon="work.isLiked ? Star : StarFilled"
              :type="work.isLiked ? 'warning' : 'info'"
              circle
            />
            <span class="like-count">{{ work.likes }}</span>
            <el-button
              size="small"
              :icon="ChatLineRound"
              @click="viewWorkDetail(work)"
              type="primary"
              circle
            />
            <span class="comment-count">{{ work.comments }}</span>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 5. 分页控件 -->
    <div class="pagination-container">
      <el-pagination 
        layout="prev, pager, next" 
        :total="filteredWorks.length"
        :page-size="12"
        @current-change="handlePageChange"
      />
    </div>
    
    <!-- 6. 发布作品弹窗 -->
    <el-dialog v-model="publishDialogVisible" title="发布新作品" width="500px">
      <el-form :model="newWork" label-position="top">
        <el-form-item label="作品标题" required>
          <el-input v-model="newWork.title" placeholder="请输入作品标题"></el-input>
        </el-form-item>
        
        <el-form-item label="作品分类" required>
          <el-select v-model="newWork.category" placeholder="请选择作品分类" style="width: 100%">
            <el-option label="Scratch作品" value="scratch" />
            <el-option label="Python作品" value="python" />
            <el-option label="Web作品" value="web" />
            <el-option label="游戏作品" value="game" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="作品描述">
          <el-input 
            v-model="newWork.description" 
            type="textarea" 
            rows="3"
            placeholder="请简要描述你的创意和玩法"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="封面图片">
          <el-input v-model="newWork.cover" placeholder="请输入图片URL（可用在线图片）"></el-input>
        </el-form-item>
        
        <el-form-item label="标签">
          <el-select
            v-model="newWork.tags"
            multiple
            placeholder="选择或创建标签"
            style="width: 100%"
          >
            <el-option label="游戏" value="游戏" />
            <el-option label="动画" value="动画" />
            <el-option label="故事" value="故事" />
            <el-option label="艺术" value="艺术" />
            <el-option label="音乐" value="音乐" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="publishDialogVisible = false">取消</el-button>
          <el-button type="success" @click="publishWork">发布作品</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 7. 作品详情弹窗 -->
    <el-dialog v-model="detailDialogVisible" title="作品详情" width="700px" v-if="selectedWork">
      <div class="work-detail">
        <div class="detail-header">
          <img :src="selectedWork.cover" :alt="selectedWork.title" class="detail-cover">
          <div class="detail-info">
            <h2>{{ selectedWork.title }}</h2>
            <p>
              <el-icon style="color: #60a5fa;"><UserFilled /></el-icon>
              作者: {{ selectedWork.author }}
            </p>
            <p>分类: {{ getCategoryName(selectedWork.category) }}</p>
            <p>发布时间: {{ selectedWork.createTime }}</p>
            <div class="detail-stats">
              <span>👍 {{ selectedWork.likes }} 赞</span>
              <span>💬 {{ selectedWork.comments }} 评论</span>
            </div>
          </div>
        </div>
        
        <div class="detail-description">
          <h3>作品介绍</h3>
          <p>{{ selectedWork.description }}</p>
        </div>
        
        <div class="detail-tags">
          <el-tag v-for="tag in selectedWork.tags" :key="tag" size="small" class="tag-item" type="success">
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Star, StarFilled, ChatLineRound, UserFilled } from '@element-plus/icons-vue'

// 筛选与搜索数据
const searchQuery = ref('')
const filterCategory = ref('')
const currentPage = ref(1)

// 弹窗控制
const publishDialogVisible = ref(false)
const detailDialogVisible = ref(false)

// 选中的作品
const selectedWork = ref(null)
// 作品列表数据
const works = ref([
    {
        id: 1,
        title: '太空探险游戏',
        author: '小明',
        authorId: 101,
        category: 'scratch',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/太空探险',
        description: '这是一个使用Scratch创建的太空冒险游戏，你需要控制飞船躲避陨石。',
        likes: 42,
        comments: 8,
        createTime: '2025-06-28',
        tags: ['游戏', 'Scratch', '太空']
    },
    {
        id: 2,
        title: '贪吃蛇',
        author: '小红',
        authorId: 102,
        category: 'python',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/贪吃蛇',
        description: '用Python实现的经典贪吃蛇游戏，有趣又好玩！',
        likes: 36,
        comments: 5,
        createTime: '2025-06-25',
        tags: ['游戏', 'Python', '经典']
    },
    {
        id: 3,
        title: '个人网站',
        author: '小李',
        authorId: 103,
        category: 'web',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/个人网站',
        description: '我的第一个个人网站，使用HTML和CSS制作。',
        likes: 28,
        comments: 6,
        createTime: '2025-06-20',
        tags: ['网站', 'HTML', 'CSS']
    },
    {
        id: 4,
        title: '音乐播放器',
        author: '小张',
        authorId: 104,
        category: 'web',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/音乐播放器',
        description: '一个漂亮的音乐播放器，支持播放、暂停、切换歌曲等功能。',
        likes: 55,
        comments: 12,
        createTime: '2025-06-27',
        tags: ['音乐', 'Web', 'JavaScript']
    },
    {
        id: 5,
        title: '小猫钓鱼',
        author: '小王',
        authorId: 105,
        category: 'scratch',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/小猫钓鱼',
        description: '可爱的小猫钓鱼游戏，操作简单，画面精美。',
        likes: 31,
        comments: 9,
        createTime: '2025-06-22',
        tags: ['游戏', 'Scratch', '动物']
    },
    {
        id: 6,
        title: '计算器',
        author: '小刘',
        authorId: 106,
        category: 'python',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/计算器',
        description: '用Python Tkinter制作的图形界面计算器，支持基本运算。',
        likes: 24,
        comments: 4,
        createTime: '2025-06-18',
        tags: ['工具', 'Python', 'GUI']
    },
    {
        id: 7,
        title: '彩虹动画',
        author: '小陈',
        authorId: 107,
        category: 'scratch',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/彩虹动画',
        description: '绚丽的彩虹动画效果，展示Scratch的图形编程能力。',
        likes: 38,
        comments: 7,
        createTime: '2025-06-26',
        tags: ['动画', 'Scratch', '艺术']
    },
    {
        id: 8,
        title: '待办事项应用',
        author: '小周',
        authorId: 108,
        category: 'web',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/待办事项',
        description: '简洁实用的待办事项管理应用，可以添加、删除和标记完成任务。',
        likes: 45,
        comments: 11,
        createTime: '2025-06-24',
        tags: ['工具', 'Web', '生产力']
    },
    {
        id: 9,
        title: '猜数字游戏',
        author: '小吴',
        authorId: 109,
        category: 'python',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/猜数字',
        description: '经典的猜数字游戏，系统随机生成数字，你来猜！',
        likes: 19,
        comments: 3,
        createTime: '2025-06-15',
        tags: ['游戏', 'Python', '逻辑']
    },
    {
        id: 10,
        title: '飞机大战',
        author: '小郑',
        authorId: 110,
        category: 'game',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/飞机大战',
        description: '刺激的飞机大战游戏，消灭敌机，获得高分！',
        likes: 67,
        comments: 15,
        createTime: '2025-06-29',
        tags: ['游戏', '射击', '动作']
    },
    {
        id: 11,
        title: '电子相册',
        author: '小林',
        authorId: 111,
        category: 'web',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/电子相册',
        description: '美丽的电子相册，展示我的摄影作品和回忆。',
        likes: 33,
        comments: 8,
        createTime: '2025-06-21',
        tags: ['相册', 'Web', '摄影']
    },
    {
        id: 12,
        title: '数字时钟',
        author: '小黄',
        authorId: 112,
        category: 'python',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/数字时钟',
        description: '炫酷的数字时钟显示，实时更新时间。',
        likes: 26,
        comments: 5,
        createTime: '2025-06-19',
        tags: ['时钟', 'Python', '工具']
    },
    {
        id: 13,
        title: '迷宫探险',
        author: '小徐',
        authorId: 113,
        category: 'scratch',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/迷宫探险',
        description: '挑战性的迷宫游戏，找到出口获得胜利！',
        likes: 41,
        comments: 10,
        createTime: '2025-06-23',
        tags: ['游戏', 'Scratch', '迷宫']
    },
    {
        id: 14,
        title: '天气预报',
        author: '小孙',
        authorId: 114,
        category: 'web',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/天气预报',
        description: '实用的天气预报应用，查看各地天气情况。',
        likes: 52,
        comments: 13,
        createTime: '2025-06-28',
        tags: ['天气', 'Web', '实用']
    },
    {
        id: 15,
        title: '数据可视化',
        author: '小马',
        authorId: 115,
        category: 'python',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/数据可视化',
        description: '使用Python制作的数据可视化图表，展示统计数据。',
        likes: 39,
        comments: 6,
        createTime: '2025-06-17',
        tags: ['数据', 'Python', '图表']
    },
    {
        id: 16,
        title: '俄罗斯方块',
        author: '小朱',
        authorId: 116,
        category: 'game',
        cover: 'https://placeholder.pics/svg/300x200/DEDEDE/555555/俄罗斯方块',
        description: '经典的俄罗斯方块游戏，挑战你的反应速度！',
        likes: 73,
        comments: 18,
        createTime: '2025-06-30',
        tags: ['游戏', '经典', '方块']
    }
])

// 新作品表单数据
const newWork = reactive({
  title: '',
  category: '',
  description: '',
  cover: '',
  tags: []
})

// 根据筛选条件过滤作品
const filteredWorks = computed(() => {
  return works.value.filter(work => {
    // 按分类筛选
    if (filterCategory.value && work.category !== filterCategory.value) {
      return false
    }
    // 按搜索词筛选
    if (searchQuery.value && !work.title.toLowerCase().includes(searchQuery.value.toLowerCase())) {
      return false
    }
    return true
  })
})

const pageSize = 12
const pagedWorks = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredWorks.value.slice(start, start + pageSize)
})

// 页面变化处理
const handlePageChange = (page: number) => {
  currentPage.value = page
}

// 查看作品详情
const viewWorkDetail = (work: any) => {
  selectedWork.value = work
  detailDialogVisible.value = true
}

// 显示发布对话框
const showPublishDialog = () => {
  Object.assign(newWork, {
    title: '',
    category: '',
    description: '',
    cover: '',
    tags: []
  })
  publishDialogVisible.value = true
}

// 发布作品
const publishWork = () => {
  if (!newWork.title || !newWork.category) {
    ElMessage.warning('请填写必要的作品信息')
    return
  }
  ElMessage.success('作品发布成功!')
  publishDialogVisible.value = false
  const newId = works.value.length + 1
  works.value.unshift({
    id: newId,
    title: newWork.title,
    author: '当前用户',
    authorId: 999,
    category: newWork.category,
    cover: newWork.cover || 'https://placeholder.pics/svg/300x200/DEDEDE/555555/新作品',
    description: newWork.description,
    likes: 0,
    comments: 0,
    createTime: new Date().toISOString().split('T')[0],
    tags: newWork.tags
  })
}

// 点赞功能
const likeWork = (work: any) => {
  if (work.isLiked) {
    work.likes--
    work.isLiked = false
    ElMessage({
      message: '已取消点赞',
      type: 'info',
      duration: 1000
    })
  } else {
    work.likes++
    work.isLiked = true
    ElMessage({
      message: '点赞成功',
      type: 'success',
      duration: 1000
    })
  }
}

// 分类颜色
const getCategoryColor = (category: string) => {
  switch (category) {
    case 'scratch': return 'warning'
    case 'python': return 'success'
    case 'web': return 'info'
    case 'game': return 'danger'
    default: return 'default'
  }
}

// 获取分类名称
const getCategoryName = (category: string) => {
  const categoryMap: Record<string, string> = {
    'scratch': 'Scratch',
    'python': 'Python',
    'web': 'Web开发',
    'game': '游戏开发'
  }
  return categoryMap[category] || '其他'
}


</script>

<style scoped>
.share-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  background: rgba(255,255,255,0.96); 
  min-height: 100vh;
  box-shadow: 0 0 20px rgba(0,0,0,0.05);
  border-radius: 0;
}

/* 移除或禁用背景层，避免影响滚动 */
.share-page::before {
  display: none;
}

/* 修复页面标题区的margin */
.page-header {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
  margin-bottom: 24px;
  margin-top: 0; 
  padding-top: 20px; 
}

.page-header h1 {
  font-size: 32px;
  color: #f59e42;
  margin: 0;
  font-family: 'Comic Sans MS', '幼圆', cursive;
  letter-spacing: 2px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.publish-btn {
  white-space: nowrap;
  font-size: 16px;
  padding: 8px 20px;
  border-radius: 20px;
  background: linear-gradient(90deg, #fbbf24 0%, #34d399 100%);
  border: none;
  color: white;
  box-shadow: 0 2px 8px rgba(251,191,36,0.15);
}
/*此处不使用全局渐变色 不然太花了 */
.filter-sticky {
  position: sticky;
  top: 64px;
  z-index: 20;
  /* background: linear-gradient(135deg, #f0f9ff 0%, #fef6e4 100%); */
  background: rgba(255,255,255,0.92);
  box-shadow: 0 2px 8px rgba(251,191,36,0.04);
  padding: 12px 0;
  margin-bottom: 18px;
  margin-top: 0;
  border-radius: 8px;
}

.filter-container {
  padding: 0 0 0 0;
  margin: 0;
  background: none;
  box-shadow: none;
}

.filter-section {
  display: flex;
  gap: 16px;
  margin-bottom: 14px;
  padding: 14px 18px 10px 18px;
  background: rgba(255,255,255,0.85);
  border-radius: 16px 16px 0 0;
  box-shadow: 0 2px 8px rgba(251,191,36,0.04);
  flex-wrap: wrap;
  border-bottom: 1.5px solid #ffe7c2;
}

.search-input {
  width: 340px;
  max-width: 100%;
  min-width: 180px;
  border-radius: 24px;
  background: linear-gradient(135deg, #fffbe9 0%, #fff8f0 100%);
  border: 2px solid #ffe7c2;
  box-shadow: 0 3px 12px rgba(251,191,36,0.1);
  transition: all 0.3s ease;
  font-size: 16px;
  padding-left: 16px;
  height: 42px;
}

.search-input:focus-within {
  border-color: #fbbf24;
  box-shadow: 0 0 0 3px rgba(251,191,36,0.2), 0 4px 16px rgba(251,191,36,0.15);
  transform: translateY(-1px);
}

.search-input:hover {
  border-color: #fbbf24;
  box-shadow: 0 4px 16px rgba(251,191,36,0.12);
}

.filter-select {
  width: 160px;
  border-radius: 16px;
  min-width: 120px;
}

.tips-banner {
  display: flex;
  align-items: center;
  background: linear-gradient(90deg, #fffbe9 0%, #e0f7fa 100%);
  border-radius: 0 0 16px 16px;
  padding: 14px 24px 14px 22px;
  margin-bottom: 0;
  font-size: 17px;
  color: #f59e42;
  box-shadow: 0 4px 16px rgba(251,191,36,0.08);
  font-family: 'Comic Sans MS', '幼圆', cursive;
  border-top: 1.5px solid #ffe7c2;
  min-height: 44px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.tips-banner .el-icon {
  margin-right: 8px;
  font-size: 22px;
  color: #fbbf24;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .publish-btn {
    align-self: flex-end;
  }
  
  .filter-section {
    flex-direction: column;
    gap: 12px;
    padding: 12px 8px 8px 8px;
    border-radius: 12px 12px 0 0;
  }
  .tips-banner {
    padding: 12px 10px 12px 12px;
    border-radius: 0 0 12px 12px;
    font-size: 15px;
  }
}

.works-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 28px;
  margin-bottom: 32px;
}

.work-card {
  transition: transform 0.3s cubic-bezier(.34,1.56,.64,1);
  height: 100%;
  border-radius: 18px;
  overflow: hidden;
  background: #fffbe9;
  border: 2px solid #ffe7c2;
  box-shadow: 0 4px 16px rgba(251,191,36,0.08);
  position: relative;
}

.work-card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 8px 32px rgba(251,191,36,0.18);
}

.work-cover {
  height: 180px;
  overflow: hidden;
  cursor: pointer;
  position: relative;
background: linear-gradient(135deg, #f0f9ff 0%, #fef6e4 100%);
}

.work-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
  border-bottom: 2px solid #ffe7c2;
}

.work-cover:hover img {
  transform: scale(1.07);
}

.cover-badge {
  position: absolute;
  top: 10px;
  left: 10px;
}

.work-info {
  padding: 18px 16px 12px 16px;
}

.work-title {
  margin: 0 0 8px;
  font-size: 20px;
  cursor: pointer;
  color: #f59e42;
  font-family: 'Comic Sans MS', '幼圆', cursive;
  display: flex;
  align-items: center;
  gap: 4px;
}

.work-title:hover {
  color: #34d399;
}

.work-author {
  font-size: 15px;
  color: #60a5fa;
  margin: 0 0 8px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.work-meta {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
  font-size: 13px;
  color: #999;
}

.work-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.like-count, .comment-count {
  font-size: 15px;
  color: #f59e42;
  margin-right: 8px;
  margin-left: 2px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin: 32px 0;
}

/* 作品详情样式 */
.work-detail {
  color: #333;
}

.detail-header {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
}

.detail-cover {
  width: 300px;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  border: 2px solid #ffe7c2;
  background: #f0f9ff;
}

.detail-info {
  flex: 1;
}

.detail-info h2 {
  margin-top: 0;
  margin-bottom: 12px;
  color: #f59e42;
  font-family: 'Comic Sans MS', '幼圆', cursive;
}

.detail-stats {
  margin-top: 16px;
  display: flex;
  gap: 16px;
  font-size: 15px;
  color: #f59e42;
}

.detail-description {
  margin-bottom: 24px;
}

.detail-description h3 {
  margin-bottom: 12px;
  font-size: 18px;
  color: #34d399;
}

.detail-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.tag-item {
  margin-right: 0;
  font-size: 14px;
}
</style>