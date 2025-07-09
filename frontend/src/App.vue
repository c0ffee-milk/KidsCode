<template>
  <div class="side-decor left">
    <!-- 左侧装饰：可用SVG、PNG或emoji等 -->
    <img src="@/assets/decor_robot.png" alt="机器人" class="decor-icon" />
    <img src="@/assets/decor_code.png" alt="代码块" class="decor-icon" />
    <div class="tip">开心coding！</div>
  </div>
  <div class="side-decor right">
    <!-- 右侧装饰 -->
    <img src="@/assets/decor_cat.png" alt="猫咪" class="decor-icon" />
    <img src="@/assets/decor_rocket.png" alt="火箭" class="decor-icon" />
    <div class="tip">健康growing！</div>
  </div>

  <header class="app-header">
    <div class="header-content">
      <div class="logo-section">
        <img src="/favicon.ico" class="app-logo" />
        <span class="app-title">CodeForKids</span>
        <span class="app-subtitle">少儿编程平台</span>
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
          </el-sub-menu>

         <!-- 用户中心 - 一级菜单（下拉包含登录注册） -->
        <el-sub-menu index="user">
          <template #title>
        <el-icon><User /></el-icon>用户中心
          </template>
          <el-menu-item index="/user/login">
            <el-icon><Key /></el-icon>登录
          </el-menu-item>
          <el-menu-item index="/user/register">
            <el-icon><UserFilled /></el-icon>注册
          </el-menu-item>
          <el-menu-item index="/user/report">
            <el-icon><User /></el-icon>个人中心
          </el-menu-item>
        </el-sub-menu>

        </el-menu>
      </nav>
    </div>
  </header>

  <main class="app-main">
    <router-view />
  </main>

  <footer class="app-footer">
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
  </footer>

  <el-backtop :right="50" :bottom="50" />
</template>

<script setup lang="ts">
import { useUserStore } from './stores/user';
const userStore = useUserStore();
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

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f8fafc;
  color: #1a202c;
  line-height: 1.6;
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
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1600px; /* 扩大容器宽度 */
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px; /* 增加左右padding */
  height: 80px; /* 增加高度 */
  min-width: 1400px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  min-width: 200px; /* 增加logo区域宽度 */
}

.app-logo {
  width: 42px; /* 稍微增大logo */
  height: 42px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.app-title {
  font-size: 22px; /* 增大标题字体 */
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-subtitle {
  font-size: 13px; /* 稍微增大副标题 */
  color: #64748b;
  margin-left: 8px;
}

.nav-section {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 900px; /* 原来可能是1000px或更大，改小一点 */
  margin: 0 10px;
}

.app-menu {
  background: transparent;
  border-bottom: none;
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: flex-start; /* 改为左对齐或space-between都可以 */
  gap: 12px; /* 原来gap可能太大，建议8px~16px之间 */
}

.app-menu .el-menu-item,
.app-menu .el-sub-menu {
  min-width: 70px; /* 原来可能95px或更大，适当减小 */
  padding: 0 8px; /* 原来14px，适当减小 */
  margin: 0 2px;
  font-size: 15px;
}

.app-menu .el-sub-menu .el-sub-menu__title {
  height: 44px;
  line-height: 44px;
  border-radius: 10px;
  padding: 0 14px;
  display: flex;
  align-items: center;
  min-width: 125px; /* 增加下拉菜单最小宽度 */
  justify-content: center;
}

.app-menu .el-menu-item .el-icon,
.app-menu .el-sub-menu .el-icon {
  margin-right: 6px; /* 稍微减少图标间距 */
  font-size: 16px;
  flex-shrink: 0;
}

.app-menu .el-menu-item:hover,
.app-menu .el-sub-menu:hover .el-sub-menu__title {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.app-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* 下拉菜单样式 */
.app-menu .el-sub-menu .el-menu {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(12px);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(226, 232, 240, 0.8);
  padding: 8px 0;
  margin-top: 8px;
  min-width: 180px;
}

.app-menu .el-sub-menu .el-menu .el-menu-item {
  height: 38px;
  line-height: 38px;
  margin: 2px 8px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  padding: 0 12px;
  min-width: auto;
}

.app-menu .el-sub-menu .el-menu .el-menu-item:hover {
  background: rgba(102, 126, 234, 0.08);
  color: #667eea;
  transform: none;
  box-shadow: none;
}

/* 主内容区 - 全宽度，不限制宽度 */
.app-main {
  flex: 1;
  width: 100%;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
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
  width: 240px;   /* 放大图片 */
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
