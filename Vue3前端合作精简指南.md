# Vue3前端合作精简指南

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

### 页面（views）开发流程

1. **创建视图文件**
   - 在`src/views`目录下新建`.vue`文件

2. **编写模板**
   - 在`<template>`标签中编写页面HTML结构

3. **添加样式**
   - 在`<style>`标签中编写CSS样式

4. **实现逻辑**
   - 在`<script setup>`中编写组件逻辑(TypeScript)

5. **配置路由**
   - 在`frontend/src/router/index.ts`中添加路由配置
     ```typescript
     import { createRouter, createWebHistory } from 'vue-router';
     import HomeView from '../views/HomeView.vue';
     import AboutView from '../views/AboutView.vue';
     import YourView from '../views/YourView.vue';

     const router = createRouter({
       history: createWebHistory(import.meta.env.BASE_URL),
       routes: [
         {
           path: '/',
           name: 'home',
           component: HomeView
         },
         {
           path: '/about',
           name: 'about',
           component: AboutView
         },
         {
           path: '/your-view',
           name: 'your-view',
           component: YourView
         }
       ]
     });
