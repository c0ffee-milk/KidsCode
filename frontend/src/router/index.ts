import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import LoginView from '@/views/user/Login.vue'
import SetPasswordView from '@/views/user/SetUserInfo.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  // 课程学习
  { path: '/learn/scratch', name: 'LearnScratch', component: () => import('@/views/learn/ScratchView.vue') },
  { path: '/learn/python', name: 'LearnPython', component: () => import('@/views/learn/PythonView.vue') },
  { path: '/learn/web', name: 'LearnWeb', component: () => import('@/views/learn/WebView.vue') },
  { path: '/learn/game', name: 'LearnGame', component: () => import('@/views/learn/GameView.vue') },
 
  // 社区
  { path: '/community/share', name: 'CommunityShare', component: () => import('@/views/community/Share.vue') },
  { path: '/community/forum', name: 'CommunityForum', component: () => import('@/views/community/Forum.vue') },
  { path: '/community/competition', name: 'CommunityCompetition', component: () => import('@/views/community/Competition.vue') },
  { path: '/community/competitioncenter',name:'CommunityCompetitionCenter', component: () => import('@/views/community/CompetitionCenter.vue')},
  // 用户中心
  { path: '/user/report', name: 'UserReport', component: () => import('@/views/user/Report.vue') },
  { path: '/user/profile', name: 'UserProfile', component: () => import('@/views/user/Profile.vue')},
  { path: '/user/set', name: 'UserSet', component: () => import('@/views/user/SetUserInfo.vue')},
  // 登录
  { path: '/login', name: 'Login', component: LoginView },
  // 404
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
