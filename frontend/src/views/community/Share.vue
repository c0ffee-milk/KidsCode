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
        cover: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.20B5j_rpy07YqoPrPvvSCgHaE7?w=232&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3',
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
        cover: 'https://tse4-mm.cn.bing.net/th/id/OIP-C.AeJsNYnFJ15DKJezrpRd9wHaEK?w=315&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7',
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
        cover: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.UySbcVMFoTgIVHuMxhwc1AHaFj?w=197&h=148&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3',
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
        cover: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.4lW2PH6ZrKcRRUHaf47FTQHaD2?w=329&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7',
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
        cover: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.cVdVn8d-L1aiOlXw_D8BCQHaHa?w=162&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3',
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
        cover: 'https://tse3-mm.cn.bing.net/th/id/OIP-C.hQIvJ0tfQRvAFu2WDjEm2AHaEg?w=319&h=193&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3',
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
        cover: 'https://pic.616pic.com/bg_w1180/00/03/81/v6PXKBy8e6.jpg',
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
        cover: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.2pdu1VKwWma-xD1fLP-uxQHaFK?w=279&h=194&c=7&r=0&o=5&dpr=1.5&pid=1.7',
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
        cover: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.t6LW550BmWg_ql0tPFBFjwHaE8?w=230&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3',
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
        cover: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.pCYSEbmPkrSba7Bu4vVZBAHaD_?w=197&h=106&c=7&r=0&o=5&dpr=1.5&pid=1.7',
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
        cover: 'data:image/webp;base64,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',
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
        cover: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.yHGAieVo97s_It6Wa47IrgHaDf?w=330&h=164&c=7&r=0&o=5&dpr=1.5&pid=1.7',
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
        cover: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.O-cmYdMLwMCFiDByC705AwHaER?w=300&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3',
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
        cover: 'https://cdn.pixabay.com/photo/2020/02/05/09/02/cloud-4820504_1280.jpg',
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
        cover: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.rLgtQCdx64doe7N-LY-hIQHaE7?w=268&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7',
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
        cover: 'data:image/webp;base64,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',
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