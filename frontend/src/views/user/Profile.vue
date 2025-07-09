<template>
  <div class="profile-page">
    <div class="profile-container">
      <!-- 个人信息卡片 -->
      <el-card class="profile-header-card">
        <div class="profile-header">
          <div class="avatar-section">
            <el-upload
              class="avatar-uploader"
              action=""
              :show-file-list="false"
              :before-upload="beforeAvatarUpload"
              :http-request="uploadAvatar"
            >
              <el-avatar
                :size="120"
                :src="userInfo.avatar"
                class="profile-avatar"
              >
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="avatar-overlay">
                <el-icon><Camera /></el-icon>
                <span>更换头像</span>
              </div>
            </el-upload>
          </div>
          <div class="basic-info">
            <h2 class="username">{{ userInfo.username }}</h2>
            <p class="user-title">{{ userInfo.title }}</p>
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-number">{{ userInfo.totalLearningTime }}</span>
                <span class="stat-label">学习时长(小时)</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userInfo.completedProjects }}</span>
                <span class="stat-label">完成项目</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userInfo.earnedBadges }}</span>
                <span class="stat-label">获得徽章</span>
              </div>
            </div>
          </div>
          <div class="level-section">
            <div class="level-info">
              <span class="level-text">等级 {{ userInfo.level }}</span>
              <span class="exp-text">{{ userInfo.currentExp }}/{{ userInfo.nextLevelExp }} EXP</span>
            </div>
            <el-progress
              :percentage="expPercentage"
              :stroke-width="8"
              :show-text="false"
              class="exp-progress"
            />
          </div>
        </div>
      </el-card>

      <!-- 主要内容区域 -->
      <div class="profile-content">
        <!-- 左侧菜单 -->
        <div class="profile-sidebar">
          <el-menu
            :default-active="activeTab"
            @select="handleTabChange"
            class="profile-menu"
          >
            <el-menu-item index="basic">
              <el-icon><User /></el-icon>
              <span>基本信息</span>
            </el-menu-item>
            <el-menu-item index="learning">
              <el-icon><Reading /></el-icon>
              <span>学习记录</span>
            </el-menu-item>
            <el-menu-item index="achievements">
              <el-icon><Medal /></el-icon>
              <span>成就徽章</span>
            </el-menu-item>
            <el-menu-item index="projects">
              <el-icon><FolderOpened /></el-icon>
              <span>我的项目</span>
            </el-menu-item>
            <el-menu-item index="settings">
              <el-icon><Setting /></el-icon>
              <span>账号设置</span>
            </el-menu-item>
          </el-menu>
        </div>

        <!-- 右侧内容 -->
        <div class="profile-main">
          <!-- 基本信息 -->
          <div v-if="activeTab === 'basic'" class="tab-content">
            <el-card class="info-card">
              <template #header>
                <div class="card-header">
                  <span>个人信息</span>
                  <el-button type="primary" @click="editMode = !editMode">
                    {{ editMode ? '保存' : '编辑' }}
                  </el-button>
                </div>
              </template>
              <el-form :model="userInfo" label-width="100px" class="profile-form">
                <el-form-item label="用户名">
                  <el-input v-model="userInfo.username" :disabled="!editMode" />
                </el-form-item>
                <el-form-item label="真实姓名">
                  <el-input v-model="userInfo.realName" :disabled="!editMode" />
                </el-form-item>
                <el-form-item label="年龄">
                  <el-input-number v-model="userInfo.age" :min="6" :max="18" :disabled="!editMode" />
                </el-form-item>
                <el-form-item label="性别">
                  <el-radio-group v-model="userInfo.gender" :disabled="!editMode">
                    <el-radio label="male">男</el-radio>
                    <el-radio label="female">女</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="学校">
                  <el-input v-model="userInfo.school" :disabled="!editMode" />
                </el-form-item>
                <el-form-item label="个人简介">
                  <el-input
                    type="textarea"
                    v-model="userInfo.bio"
                    :rows="4"
                    :disabled="!editMode"
                    placeholder="介绍一下你自己吧..."
                  />
                </el-form-item>
              </el-form>
            </el-card>
          </div>

          <!-- 学习记录 -->
          <div v-if="activeTab === 'learning'" class="tab-content">
            <el-card class="learning-card">
              <template #header>
                <span>学习统计</span>
              </template>
              <div class="learning-stats">
                <div class="stat-card">
                  <div class="stat-icon">
                    <el-icon><Clock /></el-icon>
                  </div>
                  <div class="stat-info">
                    <span class="stat-value">{{ userInfo.totalLearningTime }}h</span>
                    <span class="stat-desc">总学习时长</span>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon">
                    <el-icon><Trophy /></el-icon>
                  </div>
                  <div class="stat-info">
                    <span class="stat-value">{{ userInfo.completedCourses }}</span>
                    <span class="stat-desc">完成课程</span>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon">
                    <el-icon><Star /></el-icon>
                  </div>
                  <div class="stat-info">
                    <span class="stat-value">{{ userInfo.averageScore }}</span>
                    <span class="stat-desc">平均分数</span>
                  </div>
                </div>
              </div>
            </el-card>

            <el-card class="recent-activity-card">
              <template #header>
                <span>最近学习活动</span>
              </template>
              <el-timeline class="activity-timeline">
                <el-timeline-item
                  v-for="activity in recentActivities"
                  :key="activity.id"
                  :timestamp="activity.time"
                  :type="activity.type"
                >
                  <el-card class="activity-item">
                    <div class="activity-content">
                      <el-icon :class="activity.icon">
                        <component :is="activity.icon" />
                      </el-icon>
                      <div class="activity-text">
                        <h4>{{ activity.title }}</h4>
                        <p>{{ activity.description }}</p>
                      </div>
                    </div>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </el-card>
          </div>

          <!-- 成就徽章 -->
          <div v-if="activeTab === 'achievements'" class="tab-content">
            <el-card class="achievements-card">
              <template #header>
                <span>成就徽章 ({{ userInfo.earnedBadges }}/{{ totalBadges }})</span>
              </template>
              <div class="badges-grid">
                <div
                  v-for="badge in badges"
                  :key="badge.id"
                  :class="['badge-item', { earned: badge.earned }]"
                  @click="showBadgeDetail(badge)"
                >
                  <div class="badge-icon">
                    <el-icon><Medal /></el-icon>
                  </div>
                  <div class="badge-info">
                    <h4>{{ badge.name }}</h4>
                    <p>{{ badge.description }}</p>
                    <span v-if="badge.earned" class="earned-date">
                      获得于 {{ badge.earnedDate }}
                    </span>
                  </div>
                </div>
              </div>
            </el-card>
          </div>

          <!-- 我的项目 -->
          <div v-if="activeTab === 'projects'" class="tab-content">
            <el-card class="projects-card">
              <template #header>
                <div class="card-header">
                  <span>我的项目</span>
                  <el-button type="primary" @click="createProject">
                    <el-icon><Plus /></el-icon>
                    新建项目
                  </el-button>
                </div>
              </template>
              <div class="projects-grid">
                <div
                  v-for="project in projects"
                  :key="project.id"
                  class="project-item"
                  @click="openProject(project)"
                >
                  <div class="project-cover">
                    <img :src="project.cover" :alt="project.name" />
                  </div>
                  <div class="project-info">
                    <h4>{{ project.name }}</h4>
                    <p>{{ project.description }}</p>
                    <div class="project-meta">
                      <span class="project-type">{{ project.type }}</span>
                      <span class="project-date">{{ project.updatedAt }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </el-card>
          </div>

          <!-- 账号设置 -->
          <div v-if="activeTab === 'settings'" class="tab-content">
            <el-card class="settings-card">
              <template #header>
                <span>账号设置</span>
              </template>
              <el-form label-width="120px" class="settings-form">
                <el-form-item label="修改密码">
                  <el-button @click="showChangePassword = true">修改密码</el-button>
                </el-form-item>
                <el-form-item label="邮箱绑定">
                  <div class="email-setting">
                    <el-input v-model="userInfo.email" disabled />
                    <el-button @click="changeEmail">更换邮箱</el-button>
                  </div>
                </el-form-item>
                <el-form-item label="隐私设置">
                  <el-switch
                    v-model="userInfo.isPublic"
                    active-text="公开资料"
                    inactive-text="私有资料"
                  />
                </el-form-item>
                <el-form-item label="学习提醒">
                  <el-switch
                    v-model="userInfo.learningReminder"
                    active-text="开启提醒"
                    inactive-text="关闭提醒"
                  />
                </el-form-item>
                <el-form-item label="消息通知">
                  <el-checkbox-group v-model="userInfo.notifications">
                    <el-checkbox label="system">系统消息</el-checkbox>
                    <el-checkbox label="achievement">成就通知</el-checkbox>
                    <el-checkbox label="community">社区动态</el-checkbox>
                  </el-checkbox-group>
                </el-form-item>
              </el-form>
            </el-card>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="showChangePassword" title="修改密码" width="400px">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef">
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input type="password" v-model="passwordForm.currentPassword" />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input type="password" v-model="passwordForm.newPassword" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input type="password" v-model="passwordForm.confirmPassword" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showChangePassword = false">取消</el-button>
        <el-button type="primary" @click="changePassword">确认修改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User, Camera, Reading, Medal, FolderOpened, Setting,
  Clock, Trophy, Star, Plus
} from '@element-plus/icons-vue'

// 响应式数据
const activeTab = ref('basic')
const editMode = ref(false)
const showChangePassword = ref(false)
const passwordFormRef = ref()

// 用户信息
const userInfo = ref({
  id: 1,
  username: 'CodeKid001',
  realName: '小明',
  age: 12,
  gender: 'male',
  school: '阳光小学',
  bio: '我是一个热爱编程的小学生，喜欢用代码创造有趣的东西！',
  avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  email: 'codekid001@example.com',
  title: '编程小达人',
  level: 5,
  currentExp: 750,
  nextLevelExp: 1000,
  totalLearningTime: 86,
  completedProjects: 12,
  earnedBadges: 8,
  completedCourses: 15,
  averageScore: 92,
  isPublic: true,
  learningReminder: true,
  notifications: ['system', 'achievement']
})

// 修改密码表单
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordRules = {
  currentPassword: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: Function) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 最近活动
const recentActivities = ref([
  {
    id: 1,
    title: '完成Python基础课程',
    description: '恭喜你完成了Python基础课程的所有章节！',
    time: '2025-01-10 14:30',
    type: 'success',
    icon: 'Trophy'
  },
  {
    id: 2,
    title: '获得"逻辑小达人"徽章',
    description: '成功解决了10个逻辑编程题目',
    time: '2025-01-09 16:20',
    type: 'warning',
    icon: 'Medal'
  },
  {
    id: 3,
    title: '创建新项目',
    description: '开始了一个新的Scratch动画项目',
    time: '2025-01-08 10:15',
    type: 'primary',
    icon: 'FolderOpened'
  }
])

// 徽章数据
const badges = ref([
  {
    id: 1,
    name: '初出茅庐',
    description: '完成第一个编程练习',
    earned: true,
    earnedDate: '2024-12-15'
  },
  {
    id: 2,
    name: '逻辑小达人',
    description: '连续解决10个逻辑题',
    earned: true,
    earnedDate: '2025-01-09'
  },
  {
    id: 3,
    name: '创意天才',
    description: '创建5个原创项目',
    earned: true,
    earnedDate: '2025-01-05'
  },
  {
    id: 4,
    name: '坚持不懈',
    description: '连续学习30天',
    earned: false,
    earnedDate: null
  },
  {
    id: 5,
    name: '分享达人',
    description: '分享10个作品到社区',
    earned: false,
    earnedDate: null
  }
])

// 项目数据
const projects = ref([
  {
    id: 1,
    name: '太空探险游戏',
    description: '一个有趣的太空冒险游戏',
    type: 'Scratch',
    cover: 'https://via.placeholder.com/200x150/667eea/white?text=Space+Game',
    updatedAt: '2025-01-10'
  },
  {
    id: 2,
    name: '计算器程序',
    description: '用Python编写的简单计算器',
    type: 'Python',
    cover: 'https://via.placeholder.com/200x150/38b2ac/white?text=Calculator',
    updatedAt: '2025-01-08'
  },
  {
    id: 3,
    name: '个人网站',
    description: '我的第一个HTML网页',
    type: 'Web',
    cover: 'https://via.placeholder.com/200x150/f56565/white?text=My+Website',
    updatedAt: '2025-01-05'
  }
])

// 计算属性
const expPercentage = computed(() => {
  return Math.floor((userInfo.value.currentExp / userInfo.value.nextLevelExp) * 100)
})

const totalBadges = computed(() => badges.value.length)

// 方法
const handleTabChange = (tab: string) => {
  activeTab.value = tab
}

const beforeAvatarUpload = (file: File) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('头像图片只能是 JPG/PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像图片大小不能超过 2MB!')
    return false
  }
  return true
}

const uploadAvatar = async (options: any) => {
  // TODO: 实现头像上传 API 调用
  try {
    const formData = new FormData()
    formData.append('avatar', options.file)
    
    // const response = await api.uploadAvatar(formData)
    // userInfo.value.avatar = response.data.avatarUrl
    
    ElMessage.success('头像上传成功!')
  } catch (error) {
    ElMessage.error('头像上传失败!')
  }
}

const changePassword = async () => {
  if (!passwordFormRef.value) return
  
  try {
    await passwordFormRef.value.validate()
    
    // TODO: 实现修改密码 API 调用
    // await api.changePassword({
    //   currentPassword: passwordForm.value.currentPassword,
    //   newPassword: passwordForm.value.newPassword
    // })
    
    ElMessage.success('密码修改成功!')
    showChangePassword.value = false
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error) {
    ElMessage.error('密码修改失败!')
  }
}

const changeEmail = async () => {
  try {
    const { value: email } = await ElMessageBox.prompt('请输入新的邮箱地址', '更换邮箱', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValidator: (value: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        return emailRegex.test(value) ? true : '请输入正确的邮箱格式'
      }
    })
    
    // TODO: 实现更换邮箱 API 调用
    // await api.changeEmail({ email })
    
    userInfo.value.email = email
    ElMessage.success('邮箱更换成功!')
  } catch (error) {
    // 用户取消操作
  }
}

const showBadgeDetail = (badge: any) => {
  ElMessageBox.alert(badge.description, badge.name, {
    confirmButtonText: '确定',
    type: badge.earned ? 'success' : 'info'
  })
}

const createProject = () => {
  // TODO: 跳转到项目创建页面
  ElMessage.info('跳转到项目创建页面')
}

const openProject = (project: any) => {
  // TODO: 跳转到项目编辑页面
  ElMessage.info(`打开项目: ${project.name}`)
}

// 生命周期
onMounted(async () => {
  // TODO: 加载用户数据
  await loadUserProfile()
})

const loadUserProfile = async () => {
  try {
    // TODO: 实现加载用户资料 API 调用
    // const response = await api.getUserProfile()
    // userInfo.value = response.data
  } catch (error) {
    ElMessage.error('加载用户资料失败!')
  }
}

// API 接口预留
const api = {
  // 获取用户资料
  getUserProfile: () => {
    // return axios.get('/api/user/profile')
  },
  
  // 更新用户资料
  updateProfile: (data: any) => {
    // return axios.put('/api/user/profile', data)
  },
  
  // 上传头像
  uploadAvatar: (formData: FormData) => {
    // return axios.post('/api/user/avatar', formData)
  },
  
  // 修改密码
  changePassword: (data: any) => {
    // return axios.post('/api/user/change-password', data)
  },
  
  // 更换邮箱
  changeEmail: (data: any) => {
    // return axios.post('/api/user/change-email', data)
  },
  
  // 获取学习记录
  getLearningHistory: () => {
    // return axios.get('/api/user/learning-history')
  },
  
  // 获取成就徽章
  getBadges: () => {
    // return axios.get('/api/user/badges')
  },
  
  // 获取项目列表
  getProjects: () => {
    // return axios.get('/api/user/projects')
  }
}
</script>

<style scoped>
.profile-page {
  min-height: calc(100vh - 160px);
  background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
  padding: 40px 0;
}

.profile-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 头部卡片 */
.profile-header-card {
  margin-bottom: 32px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 40px;
  padding: 20px 0;
}

.avatar-section {
  position: relative;
}

.avatar-uploader {
  position: relative;
  cursor: pointer;
}

.profile-avatar {
  border: 4px solid #667eea;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
  font-size: 12px;
}

.avatar-uploader:hover .avatar-overlay {
  opacity: 1;
}

.basic-info {
  flex: 1;
}

.username {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.user-title {
  font-size: 1.1rem;
  color: #667eea;
  margin-bottom: 20px;
}

.user-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
  color: #667eea;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
}

.level-section {
  min-width: 200px;
}

.level-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.level-text {
  font-weight: 600;
  color: #1e293b;
}

.exp-text {
  font-size: 0.9rem;
  color: #64748b;
}

.exp-progress {
  width: 100%;
}

/* 主要内容区域 */
.profile-content {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 32px;
}

.profile-sidebar {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 20px 0;
  height: fit-content;
}

.profile-menu {
  border: none;
}

.profile-menu .el-menu-item {
  margin: 4px 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.profile-menu .el-menu-item:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.profile-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.profile-main {
  min-height: 500px;
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 卡片样式 */
.info-card,
.learning-card,
.recent-activity-card,
.achievements-card,
.projects-card,
.settings-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 学习统计 */
.learning-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 12px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-desc {
  font-size: 0.9rem;
  color: #64748b;
}

/* 活动时间线 */
.activity-timeline {
  padding: 20px 0;
}

.activity-item {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.activity-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.activity-text h4 {
  margin-bottom: 4px;
  color: #1e293b;
}

.activity-text p {
  color: #64748b;
  font-size: 0.9rem;
}

/* 徽章网格 */
.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.badge-item {
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

.badge-item.earned {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  opacity: 1;
}

.badge-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.badge-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.badge-info h4 {
  margin-bottom: 4px;
  color: #1e293b;
}

.badge-info p {
  color: #64748b;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.earned-date {
  font-size: 0.8rem;
  color: #667eea;
  font-weight: 500;
}

/* 项目网格 */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.project-item {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  background: white;
}

.project-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

.project-cover {
  height: 150px;
  overflow: hidden;
}

.project-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.project-info {
  padding: 16px;
}

.project-info h4 {
  margin-bottom: 8px;
  color: #1e293b;
}

.project-info p {
  color: #64748b;
  font-size: 0.9rem;
  margin-bottom: 12px;
}

.project-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-type {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
}

.project-date {
  font-size: 0.8rem;
  color: #64748b;
}

/* 设置表单 */
.email-setting {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
  
  .profile-sidebar {
    order: 2;
  }
  
  .profile-menu {
    display: flex;
    overflow-x: auto;
  }
  
  .profile-menu .el-menu-item {
    margin: 4px 8px;
    min-width: 120px;
  }
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 24px;
  }
  
  .user-stats {
    justify-content: center;
  }
  
  .learning-stats {
    grid-template-columns: 1fr;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .badges-grid {
    grid-template-columns: 1fr;
  }
}
</style>