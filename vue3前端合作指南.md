# Vue3前端合作指南

## 运行

    [提示]项目已初始化vue的框架，不需要再初始化vue框架了

### 切换到前端目录

```bash
cd frontend
```

### 安装依赖

```bash
npm install
```

### 运行项目

```bash
npm run dev
```

## 敲代码

### 项目目录结构

#### 核心目录
- `src/` - 主代码目录
  - `components/` - 可复用组件
  - `views/` - 页面级组件
  - `assets/` - 静态资源(样式/图片等)
  - `router/` - 路由配置
  - `stores/` - 状态管理(Pinia)

#### 辅助目录
- `public/` - 公共静态资源
- `src/plugins/` - 插件
- `src/config/` - 项目配置
- `src/api/` - 接口定义
- `src/utils/` - 工具函数
- `src/constants/` - 常量定义
- `src/types/` - 类型定义

### 页面（views）的编写

    步骤：
    1. 在src/views文件夹中新建一个.vue文件
    2. 在.vue文件中编写页面的html代码（template部分）
    3. 在.vue文件中编写页面的css代码（style部分）
    4. 在.vue文件中编写页面的js代码（script部分）
    5. 在路由文件中添加页面的路由 frontend\src\router\index.ts
    6. 在导航栏中添加页面的导航 frontend\src\App.vue