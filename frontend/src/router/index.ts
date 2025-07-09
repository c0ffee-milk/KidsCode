import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import MineView from '@/views/MineView.vue'
import LearnView from '@/views/LearnView.vue'





const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/mine', name: 'Mine', component: MineView },
  { path: '/learn', name: 'Learn', component: LearnView },

  // 课程学习
  { path: '/learn/scratch', name: 'LearnScratch', component: () => import('@/views/learn/ScratchView.vue') },
  { path: '/learn/python', name: 'LearnPython', component: () => import('@/views/learn/PythonView.vue') },
  { path: '/learn/web', name: 'LearnWeb', component: () => import('@/views/learn/WebView.vue') },
  { path: '/learn/game', name: 'LearnGame', component: () => import('@/views/learn/GameView.vue') },

  // 练习中心
  // Make sure the file exists at the specified path, or update the path if the file is named differently
    { path: '/practice/coding', name: 'PracticeCoding', component: () => import('@/views/practice/CodingView.vue') },
  { path: '/practice/challenge', name: 'PracticeChallenge', component: () => import('@/views/practice/ChallengeView.vue') },
  { path: '/practice/project', name: 'PracticeProject', component: () => import('@/views/practice/ProjectView.vue') },

  // 社区
  { path: '/community/share', name: 'CommunityShare', component: () => import('@/views/community/Share.vue') },
  { path: '/community/forum', name: 'CommunityForum', component: () => import('@/views/community/Forum.vue') },
  { path: '/community/competition', name: 'CommunityCompetition', component: () => import('@/views/community/Competition.vue') },

  // 用户中心
  { path: '/user/login', name: 'UserLogin', component: () => import('@/views/user/Login.vue') },
  { path: '/user/register', name: 'UserRegister', component: () => import('@/views/user/Register.vue') },
  { path: '/user/report', name: 'UserReport', component: () => import('@/views/user/Report.vue') },
  {
    path: '/user/profile',
    name: 'UserProfile',
    component: () => import('@/views/user/Profile.vue')
  },
  
  // 兼容旧路径
  { path: '/login', redirect: '/user/login' },
  { path: '/register', redirect: '/user/register' },

  // 404
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
