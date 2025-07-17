<template>
  <!-- <div class="side-decor left"> -->
    <!-- 左侧装饰：可用SVG、PNG或emoji等 -->
    <!-- <img src="@/assets/decor_robot.svg" alt="机器人" class="decor-icon" />
    <img src="@/assets/decor_code.svg" alt="代码块" class="decor-icon" /> -->
    <!-- <div class="tip">开心coding！</div> -->
  <!-- </div>
  <div class="side-decor right"> -->
    <!-- 右侧装饰 -->
    <!-- <img src="@/assets/decor_cat.svg" alt="猫咪" class="decor-icon" />
    <img src="@/assets/decor_rocket.svg" alt="火箭" class="decor-icon" /> -->
    <!-- <div class="tip">健康growing！</div> -->
  <!-- </div> -->

  <header class="app-header">
    <div class="header-content">
      <div class="logo-section" @click="router.push('/')">
        <img src="/favicon.svg" class="app-logo" />
        <span class="app-title">CodeForKids</span>
      </div>
      <nav class="nav-section">
        <el-menu
          mode="horizontal"
          router="true"
          :default-active="$route.path"
          class="app-menu"
        >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>首页
          </el-menu-item>

          <!-- 课程学习 -->
          <el-sub-menu index="learn">
            <template #title>
              <el-icon><Edit /></el-icon>课程学习
            </template>
            <el-menu-item index="/learn/scratch">
              <el-icon><Compass /></el-icon>Scratch编程
            </el-menu-item>
            <el-menu-item index="/learn/python">
              <el-icon><Document /></el-icon>Python基础
            </el-menu-item>
            <el-menu-item index="/learn/web">
              <el-icon><Monitor /></el-icon>关卡选择
            </el-menu-item>
            <el-menu-item index="/learn/game">
              <el-icon><Trophy /></el-icon>游戏开发
            </el-menu-item>
          </el-sub-menu>

          <!-- 练习中心
          <el-sub-menu index="practice">
            <template #title>
              <el-icon><Cpu /></el-icon>练习中心
            </template>
            <el-menu-item index="/practice/coding">
              <el-icon><EditPen /></el-icon>编程练习
            </el-menu-item>
            <el-menu-item index="/practice/challenge">
              <el-icon><Star /></el-icon>编程挑战
            </el-menu-item>
            <el-menu-item index="/practice/project">
              <el-icon><FolderOpened /></el-icon>项目实战
            </el-menu-item>
          </el-sub-menu> -->

          <!-- 社区 -->
          <el-sub-menu index="community">
            <template #title>
              <el-icon><ChatDotSquare /></el-icon>社区
            </template>
            <el-menu-item index="/community/share">
              <el-icon><Share /></el-icon>作品分享
            </el-menu-item>
            <el-menu-item index="/community/forum">
              <el-icon><Message /></el-icon>讨论论坛
            </el-menu-item>
            <el-menu-item index="/community/competition">
              <el-icon><Medal /></el-icon>编程竞赛
            </el-menu-item>
            <el-menu-item index="/community/competitioncenter">
              <el-icon><Trophy /></el-icon>竞赛中心
            </el-menu-item>
          </el-sub-menu>

         <!-- 用户中心 - 一级菜单 -->
        <el-sub-menu v-if="userStore.token" index="user">
          <template #title>
        <el-icon><User /></el-icon>用户中心
          </template>
          <el-menu-item index="/user/report">用户画像</el-menu-item>
          <el-menu-item index="/user/profile">个人资料</el-menu-item>
          <el-menu-item index="/user/set">设置昵称和密码</el-menu-item>
          <el-menu-item index="" @click="handleLogout">退出登录</el-menu-item>
        </el-sub-menu>

        <el-menu-item v-else index="/login">
            登录
          </el-menu-item>
        </el-menu>
      </nav>
    </div>
  </header>

  <main class="app-main">
    <router-view />
  </main>

  <!-- <footer class="app-footer">
    <div class="footer-content">
      <p>© 2025 CodeForKids | 快乐学习，快乐成长</p>
      <div class="footer-links">
        <a href="#">关于我们</a>
        <a href="#">联系方式</a>
        <a href="#">帮助中心</a>
        <a href="#">隐私政策</a>
        <a href="#">用户协议</a>
      </div>
    </div>
  </footer> -->

  <el-backtop :right="50" :bottom="50" />

  <div class="ai-assistant-fab" @click="showAI = true" style="color: #fff;">
    <svg width="36" height="36" viewBox="0 0 48 48" fill="none">
      <circle cx="24" cy="24" r="20" stroke="currentColor" stroke-width="3" fill="none"/>
      <ellipse cx="24" cy="28" rx="10" ry="6" fill="currentColor" opacity="0.8"/>
      <circle cx="18" cy="22" r="2" fill="#fff"/>
      <circle cx="30" cy="22" r="2" fill="#fff"/>
      <!-- 可根据需要美化 -->
    </svg>
  </div>
  <!-- AI助手聊天框 -->
  <div v-if="showAI" class="ai-chat-overlay">
    <div class="ai-chat-container">
      <div class="ai-chat-header">
        <span>🤖 AI编程助手</span>
        <button @click="showAI = false" class="ai-close-btn">×</button>
      </div>
      <div class="ai-chat-history" ref="chatHistory">
        <div v-for="(msg, index) in aiHistory" :key="index" :class="['ai-message', msg.role]">
          <div class="message-content">{{ msg.text }}</div>
          <div v-if="msg.timestamp" class="message-time">{{ msg.timestamp }}</div>
        </div>
      </div>
      <div class="ai-chat-input-area">
        <!-- 新增代码分析按钮 -->
        <button @click="triggerCodeAnalysis" class="ai-analysis-btn" title="分析当前关卡常见错误">
          🤖 代码分析
        </button>
        <div class="ai-input-group">
          <input 
            v-model="aiInput" 
            @keyup.enter="sendAIMessage" 
            placeholder="输入你的问题..."
            class="ai-input"
          />
          <button @click="sendAIMessage" class="ai-send-btn">发送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

declare global {
  interface Window {
    showCurrentLevelErrors?: () => void
  }
}

const router = useRouter()
const userStore = useUserStore()

const handleLogout = () => {
  userStore.clear()
  router.push('/')
}

const showAI = ref(false)
const aiInput = ref('')
type AIMessage = { role: string; text: string; timestamp?: string }
const aiHistory = ref<AIMessage[]>([
  { role: 'ai', text: '你好！我是AI编程助手🤖，点击各关卡的"代码分析"按钮，我会为你分析常见错误和解决方案！' }
])

function sendAIMessage() {
  if (!aiInput.value.trim()) return
  const question = aiInput.value.trim()
  aiHistory.value.push({ role: 'user', text: question })
  // 固定问答映射
  const qaMap: Record<string, string> = {
    '如何通过第二关？': '第二关建议使用“骑士向前移动N步”积木，步数设置为10即可到达终点。',
    '如何判断障碍物？': '可以使用“当前位置是否是障碍?”判断积木，遇到障碍时选择绕行。',
    '如何使用循环？': '你可以使用“重复N次”或“先执行直到”积木，让骑士多次执行相同动作。',
    'Python是什么？': 'Python是一种简单易学的编程语言，适合初学者入门。',
    '你好': '你好！我是AI编程助手，有什么可以帮你的吗？',
    '为什么骑士撞到障碍物了？': '请检查是否在移动前用“当前位置是否是障碍?”进行判断，遇到障碍应选择绕行。',
    '为什么骑士没有到达终点？': '请确认你的循环或步数设置是否正确，终点通常在地图最右侧或指定位置。',
    '如何让骑士上下左右移动？': '可以使用“骑士向上/下/左/右移动N步”积木，参数为步数。',
    '如何判断骑士是否到达终点？': '使用“当前位置是否为终点?”判断积木，配合if语句实现。',
    '如何跳出循环？': '可以在循环内部用判断终点的积木，达到终点后用break语句跳出循环。',
    '为什么骑士走出地图了？': '请检查移动前是否判断了边界，建议加上边界判断避免越界。',
    '如何避开多个障碍？': '可以用循环+判断，每次遇到障碍时选择其它方向移动，直到通过。',
    '为什么骑士原地不动？': '请检查移动积木是否放在循环或判断内部，或步数参数是否为0。',
    '如何让骑士说话？': '可以使用“提示”积木，让骑士在舞台上显示对话。',
    '如何重置骑士位置？': '点击“重新初始化”按钮即可重置骑士到起点。',
    '为什么我的代码运行很慢？': '可能是循环次数过多或动画延时设置较大，建议优化循环逻辑。',
    '如何查看最优路径？': '运行后地图上高亮的路径即为最优路径。',
    '如何使用do-while循环？': '拖拽“先执行直到”积木，先执行动作再判断条件是否结束。',
    '如何用for循环让骑士前进？': '使用“重复N次”积木，将移动积木放入循环体内。',
    '如何判断当前位置是迷雾？': '迷雾区域地图上显示为“🌫️”，可用判断积木检测。',
    '如何切换到下一关？': '完成本关后点击“下一关”按钮即可进入下一关。',
    '为什么提示“无法到达终点”？': '说明当前路径被障碍物或迷雾阻挡，请调整路线或增加判断。',
    '如何让骑士自动寻路？': '可尝试用循环和判断组合，让骑士每次选择可行方向前进。',
    '如何保存我的编程进度？': '目前支持自动保存，刷新页面后可继续上次进度。',
    '什么是变量？': '变量是用来存储数据的容器，可以在程序中随时修改和使用。',
    '如何定义变量？': '在Python中可以直接写：x = 10，这样就定义了一个变量x。',
    '什么是条件语句？': '条件语句用于判断某个条件是否成立，根据结果执行不同的代码。',
    '如何使用if语句？': 'if 条件: 执行代码块。可以配合else和elif使用。',
    '什么是函数？': '函数是可以重复使用的代码块，可以用def关键字定义。',
    '如何定义函数？': '在Python中：def 函数名(): 执行代码。',
    '什么是列表？': '列表是一种可以存储多个数据的容器，用[]表示。',
    '如何遍历列表？': '可以用for循环：for item in 列表: 执行代码。',
    '什么是字典？': '字典是以键值对存储数据的容器，用{}表示。',
    '如何导入模块？': '使用import关键字，例如：import math。',
    '如何调试代码？': '可以逐步运行代码，查看变量值，或使用print语句输出调试信息。',
    '为什么出现语法错误？': '请检查代码拼写、缩进和标点符号是否正确。',
    '如何解决无限循环？': '请检查循环条件是否能被满足，确保有跳出循环的可能。',
    '如何让角色跳跃？': '可以设置角色的y坐标变化，或使用“跳跃”积木。',
    '如何添加背景音乐？': '在舞台设置中添加音乐文件，并在代码中播放。',
    '如何分享我的作品？': '在社区页面点击“作品分享”即可上传你的作品。',
    '如何查看排行榜？': '在竞赛中心或关卡页面可以查看排行榜。',
    '如何获得积分？': '完成关卡、参与竞赛或分享作品都可以获得积分。',
    '如何修改昵称？': '在用户中心的设置页面可以修改昵称。',
    '如何找回密码？': '在登录页面点击“忘记密码”，按照提示操作即可。',
    '如何联系老师？': '可以在帮助中心或社区论坛发帖联系老师。',
    '如何切换编程语言？': '在关卡页面选择不同的编程语言即可切换。',
    '为什么角色卡住了？': '可能是碰到障碍或边界，请检查移动逻辑。',
    '如何让角色旋转？': '使用“旋转”积木或设置角色的方向属性。',
    '如何导出代码？': '在关卡页面点击“导出代码”按钮即可下载你的代码。',
    '如何导入代码？': '在关卡页面点击“导入代码”按钮，选择你的代码文件。',
    '如何查看帮助文档？': '在页面底部或帮助中心可以找到详细的帮助文档。',
    '如何切换主题？': '在设置页面可以选择不同的界面主题。',
    '如何举报不良内容？': '在社区页面点击举报按钮，填写相关信息即可。',
    // ...你可以继续补充更多实际遇到的问题...
    '为什么我的不是第六关的最优路线呢？':'第六关推荐的最优路线如下：从起点出发后，先一直向右走，直到遇到障碍物为止。遇到障碍物时，优先选择向上绕开（如果上面没有障碍），否则尝试向下绕开。绕开障碍后，继续向右前进，每次遇到障碍都用同样的方法绕开。当你到达最右侧的终点所在列时，如果不在终点那一行，就向上或向下移动到终点。简单来说，就是“能右就右，遇到障碍就上下绕，直到终点”。建议用循环和判断语句，让骑士每次优先向右走，遇到障碍自动选择其它方向，最终顺利到达终点。',
  }

  setTimeout(() => {
    const answer = qaMap[question] || '（AI助手模拟回复）暂未收录该问题，请尝试问其它内容。'
    aiHistory.value.push({ role: 'ai', text: answer })
  }, 600)
  aiInput.value = ''
}

// 触发代码分析的方法
function triggerCodeAnalysis() {
  // 调用全局方法来显示当前关卡错误
  if (window.showCurrentLevelErrors) {
    window.showCurrentLevelErrors()
  } else {
    showAIError('请先进入编程闯关页面才能使用代码分析功能！')
  }
}

function showAIError(msg: string) {
  aiHistory.value.push({ 
    role: 'ai', 
    text: msg,
    timestamp: new Date().toLocaleTimeString()
  })
  showAI.value = true
}

// 提供给子组件使用
provide('showAIError', showAIError)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  overflow-x: hidden;
}

/* 增加少儿编程风格的动态渐变背景色 */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(120deg, #f9e7fe, #e0f7fa, #fffde7, #ffe0e7, #e7ffe0, #e0e7ff);
  background-size: 1200% 1200%;
  animation: kids-gradient-move 18s ease-in-out infinite;
  color: #1a202c;
  line-height: 1.6;
}

@keyframes kids-gradient-move {
  0% {
    background-position: 0% 50%;
  }
  25% {
    background-position: 50% 100%;
  }
  50% {
    background-position: 100% 50%;
  }
  75% {
    background-position: 50% 0%;
  }
  100% {
    background-position: 0% 50%;
  }
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: none !important;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 强制覆盖Element Plus的默认样式 */
.el-menu--horizontal {
  border-bottom: none !important;
}

/* 解决溢出问题 */
.el-menu--horizontal {
  overflow: hidden;
  white-space: nowrap;
}

.el-menu--horizontal > .el-menu-item,
.el-menu--horizontal > .el-sub-menu > .el-sub-menu__title {
  display: inline-flex;
}
.header-content {
  min-width: 1600px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px; /* 增加左右padding */
  height: 80px; /* 增加高度 */
  width: 100%;
  box-sizing: border-box;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  min-width: 200px;
  /* 增加右边距 */
  margin-right: 40px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logo-section:hover {
  transform: scale(1.02);
}

.nav-section {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 100%;
  /* 增加左边距 */
  margin-left: 120px;
}

.app-logo {
  width: 42px;
  height: 42px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.app-title {
  font-size: 22px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-section {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 100%;
  margin: 0 340px;
}

.app-menu {
  background: transparent;
  border-bottom: none;
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: flex-start;
  gap: 10px;
}

.app-menu .el-menu-item {
  border-radius: 12px !important;
  margin: 0 4px !important;
  transition: all 0.3s ease;
  color: #5a5e66;
}

.app-menu .el-menu-item:hover {
  background-color: rgba(102, 126, 234, 0.1) !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
}

.app-menu .el-menu-item.is-active {
  color: #667eea;
  font-weight: bold;
}

.app-menu .el-sub-menu .el-sub-menu__title {
  transition: all 0.3s ease;
}

.app-menu .el-sub-menu .el-sub-menu__title:hover {
  color: #667eea;
}

.el-icon {
  transition: all 0.3s ease;
}

.app-menu .el-menu-item:hover .el-icon {
  transform: scale(1.2);
}

.app-menu .el-sub-menu:hover .el-icon {
  transform: rotate(10deg);
}

/* 主内容区 - 全宽度，不限制宽度 */
.app-main {
  flex: 1;
  width: 100%;
  background: linear-gradient(135deg, #ffffff 0%, #ffffff 100%);
  min-height: calc(100vh - 160px); /* 调整最小高度适应新的header高度 */
}

.app-footer {
  width: 100%;
  background: white;
  border-top: 1px solid #e2e8f0;
  margin-top: auto;
}

.footer-content {
  max-width: 1600px; /* 与header保持一致 */
  margin: 0 auto;
  padding: 24px 32px; /* 与header padding保持一致 */
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-content p {
  color: #64748b;
  font-size: 14px;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-links a {
  color: #64748b;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: #667eea;
}

/* 左右侧装饰样式 */
.side-decor {
  position: fixed;
  top: 80px;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
}
.side-decor.left {
  left: 0;
  gap: 48px; /* 合理的间距 */
}
.side-decor.right {
  right: 0;
  gap: 48px; /* 合理的间距 */
}
.decor-icon {
  width: 225px;   /* 放大图片 */
  height: 240px;
  margin: 16px 0; /* 上下间距适当 */
  opacity: 0.88;
}
.tip {
  margin-top: 12px; /* 让tip更靠近图片 */
  font-size: 16px;  /* 字体更大 */
  color: #7a6ff0;
  background: #f3f6fd;
  border-radius: 8px;
  padding: 8px 18px;
  text-align: center;
  box-shadow: 0 2px 8px #e6e6fa40;
  font-weight: bold; /* 让tip更醒目 */
}

/* AI助手样式 */
.ai-assistant-fab {
  position: fixed;
  right: 32px;
  bottom: 32px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: transparent; /* 透明背景 */
  box-shadow: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 9999;
  border: none;
  transition: box-shadow 0.2s;
  /* 可选：鼠标悬停时加轻微阴影 */
}
.ai-assistant-fab:hover {
  box-shadow: 0 4px 16px #7a6fff33;
}
.ai-chat-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-chat-container {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  width: 90%;
  max-width: 480px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  animation: slide-in 0.4s ease-out;
}

@keyframes slide-in {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.ai-chat-header {
  background: linear-gradient(90deg, #7a6fff 0%, #67e8ff 100%);
  color: #fff;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 18px;
  border-bottom: 2px solid #e0e7ff;
}

.ai-close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 22px;
  cursor: pointer;
}

.ai-chat-history {
  padding: 16px 24px;
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ai-message {
  padding: 10px 14px;
  border-radius: 16px;
  position: relative;
  max-width: 80%;
  word-break: break-word;
}

.ai-message.ai {
  background: linear-gradient(90deg, #e0e7ff 0%, #f9e7fe 100%);
  color: #7a6fff;
  align-self: flex-start;
}

.ai-message.user {
  background: linear-gradient(90deg, #67e8ff 0%, #7a6fff 100%);
  color: #fff;
  align-self: flex-end;
}

.message-content {
  margin: 0;
}

.message-time {
  font-size: 12px;
  color: #a0aec0;
  margin-top: 4px;
  text-align: right;
}

.ai-chat-input-area {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  border-top: 1px solid #e2e8f0;
  background: rgba(248, 250, 252, 0.8);
}

.ai-analysis-btn {
  background: linear-gradient(45deg, #ff6b6b, #ff8e53);
  color: #fff;
  border: none;
  padding: 10px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 12px rgba(255, 107, 107, 0.3);
  font-weight: 600;
  align-self: flex-start;
}

.ai-analysis-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 18px rgba(255, 107, 107, 0.4);
  background: linear-gradient(45deg, #ff8e53, #ff6b6b);
}

.ai-input-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

.ai-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
}

.ai-input:focus {
  border-color: #4c97ff;
  box-shadow: 0 0 0 3px rgba(76, 151, 255, 0.1);
}

.ai-send-btn {
  background: linear-gradient(45deg, #4c97ff, #667eea);
  color: #fff;
  border: none;
  padding: 12px 20px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 12px rgba(76, 151, 255, 0.3);
  font-weight: 600;
  min-width: 60px;
}

.ai-send-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 18px rgba(76, 151, 255, 0.4);
  background: linear-gradient(45deg, #667eea, #4c97ff);
}

/* ...其他现有样式保持不变... */
</style>


