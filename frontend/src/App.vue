<template>
  <div class="app-container">
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
  </div>
</template>

<script setup lang="ts"></script>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
}
</style>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 80px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-logo {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.app-title {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-subtitle {
  font-size: 14px;
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
  height: 50px;
  line-height: 50px;
  margin: 0 8px;
  border-radius: 25px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.app-menu .el-menu-item:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.app-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.app-main {
  flex: 1;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.app-footer {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
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
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #667eea;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 16px;
    gap: 16px;
  }
  
  .app-menu {
    width: 100%;
    justify-content: center;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .app-subtitle {
    display: none;
  }
}
</style>