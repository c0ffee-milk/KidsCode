<template>
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
          <el-menu-item index="/learn">
            <el-icon><Edit /></el-icon>开始学习
          </el-menu-item>
          <el-menu-item index="/login">
            <el-icon><User /></el-icon>登录
          </el-menu-item>
          <el-menu-item index="/register">
            <el-icon><EditPen /></el-icon>注册
          </el-menu-item>
          <el-menu-item index="/mine">
            <el-icon><Postcard /></el-icon>我的
          </el-menu-item>
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
      </div>
    </div>
  </footer>
  
  <el-backtop :right="50" :bottom="50" />
</template>

<script setup lang="ts"></script>

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
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 72px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.app-title {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-subtitle {
  font-size: 12px;
  color: #64748b;
  margin-left: 8px;
}

.nav-section {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.app-menu {
  background: transparent;
  border-bottom: none;
}

.app-menu .el-menu-item {
  height: 40px;
  line-height: 40px;
  margin: 0 4px;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-weight: 500;
  color: #475569;
}

.app-menu .el-menu-item:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.app-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

/* 主内容区 - 全宽度，不限制宽度 */
.app-main {
  flex: 1;
  width: 100%;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: calc(100vh - 144px);
}

.app-footer {
  width: 100%;
  background: white;
  border-top: 1px solid #e2e8f0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
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

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 16px;
    gap: 16px;
  }
  
  .app-menu {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
    padding: 20px 16px;
  }
  
  .app-subtitle {
    display: none;
  }
  
  .app-main {
    min-height: calc(100vh - 180px);
  }
}
</style>