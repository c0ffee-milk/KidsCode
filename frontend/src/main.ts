// 1. 基础依赖
import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'

// 2. 第三方库
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 3. 状态管理
import { createPinia } from 'pinia'

// 4. 路由
import router from './router'

// 5. 初始化应用
const app = createApp(App)

// 6. 注册Element Plus图标
Object.entries(ElementPlusIconsVue).forEach(([key, component]) => {
  app.component(key, component)
})

// 7. 使用插件
app.config.globalProperties.$echarts = echarts
app.use(createPinia())
app.use(router)
app.use(ElementPlus)

// 8. 挂载应用
app.mount('#app')
