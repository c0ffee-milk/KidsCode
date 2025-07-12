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
      <div class="logo-section">
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
              <el-icon><Monitor /></el-icon>网页制作
            </el-menu-item>
            <el-menu-item index="/learn/game">
              <el-icon><Trophy /></el-icon>游戏开发
            </el-menu-item>
          </el-sub-menu>

          <!-- 练习中心 -->
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
          </el-sub-menu>

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
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const handleLogout = () => {
  userStore.clear()
  router.push('/')
}

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
  /* 确保移除所有边框 */
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
  padding: 0 32px; /* 增加左右padding */
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
}

.nav-section {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 100%;
  /* 增加左边距 */
  margin-left: 40px;
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
  margin: 0 10px;
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

/* 响应式布局 */
@media (max-width: 1400px) {
  .header-content {
    max-width: 100%;
    padding: 0 24px;
  }

  .nav-section {
    max-width: 800px;
    margin: 0 20px;
  }
}

@media (max-width: 1200px) {
  .header-content {
    padding: 0 16px;
  }

  .nav-section {
    max-width: 700px;
    margin: 0 16px;
  }

  .app-menu .el-menu-item,
  .app-menu .el-sub-menu {
    margin: 0 2px;
    padding: 0 10px;
    font-size: 14px;
    min-width: 80px;
  }

  .app-menu .el-sub-menu .el-sub-menu__title {
    padding: 0 10px;
    min-width: 100px;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 16px;
    gap: 16px;
  }

  .nav-section {
    max-width: 100%;
    margin: 0;
  }

  .app-menu {
    width: 100%;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
  }

  .app-menu .el-menu-item,
  .app-menu .el-sub-menu {
    margin: 4px;
    min-width: auto;
  }

  .logo-section {
    min-width: auto;
  }
}
</style>


