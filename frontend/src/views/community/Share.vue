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
            <el-option label="🎨 全部分类" value="" />
            <el-option label="🎯 Scratch" value="scratch" />
            <el-option label="🐍 Python" value="python" />
            <el-option label="🌐 Web开发" value="web" />
            <el-option label="🎮 游戏开发" value="game" />
          </el-select>
          <el-select v-model="sortBy" placeholder="排序方式" class="sort-select">
            <el-option label="📅 最新发布" value="newest" />
            <el-option label="👍 点赞最多" value="likes" />
            <el-option label="💬 评论最多" value="comments" />
            <el-option label="🔥 最受欢迎" value="popular" />
          </el-select>
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

//定义作品类型
interface Work {
  id: number;
  title: string;
  author: string;
  authorId: number;
  category: string;
  cover: string;
  description: string;
  likes: number;
  comments: number;
  createTime: string;
  tags: string[];
  isLiked: boolean;
}


// 筛选与搜索数据
const searchQuery = ref('')
const filterCategory = ref('')
const sortBy = ref('newest')
const currentPage = ref(1)

// 弹窗控制
const publishDialogVisible = ref(false)
const detailDialogVisible = ref(false)

// 选中的作品
const selectedWork = ref<Work | null>(null)


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
        tags: ['游戏', 'Scratch', '太空'],
        isLiked: false 
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
        tags: ['游戏', 'Python', '经典'],
        isLiked: false 
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
        tags: ['网站', 'HTML', 'CSS'],
        isLiked: false 
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
        tags: ['音乐', 'Web', 'JavaScript'],
        isLiked: false 
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
        tags: ['游戏', 'Scratch', '动物'],
        isLiked: false 
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
        tags: ['工具', 'Python', 'GUI'],
        isLiked: false 
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
        tags: ['动画', 'Scratch', '艺术'],
        isLiked: false 
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
        tags: ['工具', 'Web', '生产力'],
        isLiked: false 
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
        tags: ['游戏', 'Python', '逻辑'],
        isLiked: false 
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
        tags: ['游戏', '射击', '动作'],
        isLiked: false 
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
        tags: ['相册', 'Web', '摄影'],
        isLiked: false 
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
        tags: ['时钟', 'Python', '工具'],
        isLiked: false 
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
        tags: ['游戏', 'Scratch', '迷宫'],
        isLiked: false
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
        tags: ['天气', 'Web', '实用'],
        isLiked: false 
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
        tags: ['数据', 'Python', '图表'],
        isLiked: false 
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
        tags: ['游戏', '经典', '方块'],
        isLiked: false 
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
  let filtered = works.value.filter(work => {
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
  
  // 排序
  switch (sortBy.value) {
    case 'newest':
      filtered.sort((a, b) => new Date(b.createTime).getTime() - new Date(a.createTime).getTime())
      break
    case 'likes':
      filtered.sort((a, b) => b.likes - a.likes)
      break
    case 'comments':
      filtered.sort((a, b) => b.comments - a.comments)
      break
    case 'popular':
      filtered.sort((a, b) => (b.likes + b.comments * 2) - (a.likes + a.comments * 2))
      break
  }
  
  return filtered
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
    tags: newWork.tags,
    isLiked: false // 新增这一行
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
  padding-top: 240px; /* 增加更多顶部padding：导航栏80px + 标题区80px + 额外间距80px */
}

.page-header {
  position: fixed;
  top: 80px; /* 导航栏高度 */
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: space-between; 
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
  margin-bottom: 0;
  margin-top: 0; 
  padding: 16px 24px;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(10px);
  border-radius: 0 0 16px 16px;
  box-shadow: 0 4px 16px rgba(251,191,36,0.12);
  border: 1px solid rgba(255,231,194,0.4);
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
  top: 160px; 
  z-index: 20;
  background: rgba(255,255,255,0.92);
  box-shadow: 0 2px 8px rgba(251,191,36,0.04);
  padding: 0 0;/* 增加内边距 */
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
  padding: 16px 20px 14px 20px;
  background: rgba(255,255,255,0.9);
  border-radius: 18px 18px 0 0;
  box-shadow: 0 3px 12px rgba(251,191,36,0.06);
  flex-wrap: wrap;
  border-bottom: 2px solid #ffe7c2;
  align-items: center;
}

.search-input {
  width: 280px;
  max-width: 100%;
  min-width: 200px;
  height: 40px; /* 改为40px，与下拉框保持一致 */
  border-radius: 4px;
  background: #ffffff;
  border: 1px solid #dcdfe6;
  box-shadow: none;
  transition: border-color 0.2s;
  font-size: 15px;
  margin-bottom: 0;
}

.search-input:focus-within {
  border-color: #409eff;
  box-shadow: none;
  transform: none;
  background: #ffffff;
}

.search-input:hover {
  border-color: #c0c4cc;
  box-shadow: none;
}

/* 保持 el-input 内部组件的简约样式 */
.search-input :deep(.el-input__wrapper) {
  border-radius: 4px;
  border: none;
  background: transparent;
  box-shadow: none;
  height: 40px; /* 确保内部wrapper也是40px */
}

.search-input :deep(.el-input__wrapper):hover {
  border: none;
  box-shadow: none;
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border: none;
  box-shadow: none;
  background: transparent;
}

.filter-select, .sort-select {
  width: 150px;
  height: 40px; /* 确保外层容器也是40px */
  border-radius: 22px;
  min-width: 140px;
}

/* 为 el-select 添加样式覆盖 */
.filter-select :deep(.el-input__wrapper),
.sort-select :deep(.el-input__wrapper) {
  border-radius: 22px;
  border: 2px solid #ffe7c2;
  background: linear-gradient(135deg, #f0f9ff 0%, #fef6e4 100%);
  box-shadow: 0 2px 8px rgba(251,191,36,0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 40px; /* 确保一致的高度 */
}

.filter-select :deep(.el-input__wrapper):hover,
.sort-select :deep(.el-input__wrapper):hover {
  border-color: #f59e42;
  box-shadow: 0 3px 12px rgba(251,191,36,0.1);
}

.filter-select :deep(.el-input__wrapper.is-focus),
.sort-select :deep(.el-input__wrapper.is-focus) {
  border-color: #fbbf24;
  box-shadow: 0 0 0 3px rgba(251,191,36,0.15), 0 4px 16px rgba(251,191,36,0.12);
  background: #ffffff;
}

/* 下拉菜单样式优化 */
.filter-select :deep(.el-select-dropdown),
.sort-select :deep(.el-select-dropdown) {
  border-radius: 12px;
  border: 2px solid #ffe7c2;
  box-shadow: 0 8px 32px rgba(251,191,36,0.12);
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(8px);
}

.filter-select :deep(.el-select-dropdown__item),
.sort-select :deep(.el-select-dropdown__item) {
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 8px;
  margin: 2px 8px;
  transition: all 0.2s;
}

.filter-select :deep(.el-select-dropdown__item:hover),
.sort-select :deep(.el-select-dropdown__item:hover) {
  background: linear-gradient(135deg, #fffbe9 0%, #fff5e6 100%);
  color: #f59e42;
}

.filter-select :deep(.el-select-dropdown__item.selected),
.sort-select :deep(.el-select-dropdown__item.selected) {
  background: linear-gradient(135deg, #fbbf24 0%, #34d399 100%);
  color: white;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .share-page {
    padding-top: 280px; /* 移动端需要更多空间 */
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    height: auto; /* 移动端高度自适应 */
  }
  
  .publish-btn {
    align-self: flex-end;
  }
  
  .filter-sticky {
    top: 220px; /* 移动端调整粘性定位 */
  }
  
  .filter-section {
    flex-direction: column;
    gap: 12px;
    padding: 14px 16px 12px 16px;
    align-items: stretch;
  }
  
  .search-input, .filter-select, .sort-select {
    width: 100%;
    min-width: auto;
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