<template>
  <el-menu mode="horizontal" router="true" default-active="/">
    <el-menu-item index="/"
      ><el-icon><House /></el-icon>首页</el-menu-item
    >
    <el-menu-item index="/login"
      ><el-icon><User /></el-icon>登录</el-menu-item
    >
    <el-menu-item index="/register"
      ><el-icon><EditPen /></el-icon>注册</el-menu-item
    >
    <el-menu-item index="/mine"
      ><el-icon><Postcard /></el-icon>我的</el-menu-item
    >
  </el-menu>
  <el-divider />
  <div>
    <router-view />
    <el-backtop :right="50" :bottom="50" />
  </div>
</template>

<script setup lang="ts"></script>

<style>
.el-menu {
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.el-menu-item {
  font-size: 16px;
  border-radius: 50px;
  margin-left: 100px;
}

.el-menu-item .el-icon {
  margin-right: 8px;
}

body {
  background-color: rgb(247, 249, 249);
}
</style>
