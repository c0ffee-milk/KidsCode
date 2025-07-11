import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import LoginView from '@/views/user/Login.vue'
import SetPasswordView from '@/views/user/SetPassword.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  // 课程学习
  { path: '/learn/scratch', name: 'LearnScratch', component: () => import('@/views/learn/ScratchView.vue') },
  { path: '/learn/python', name: 'LearnPython', component: () => import('@/views/learn/PythonView.vue') },
  { path: '/learn/web', name: 'LearnWeb', component: () => import('@/views/learn/WebView.vue') },
  { path: '/learn/game', name: 'LearnGame', component: () => import('@/views/learn/GameView.vue') },
  // 练习中心
  { path: '/practice/coding', name: 'PracticeCoding', component: () => import('@/views/practice/CodingView.vue') },
  { path: '/practice/challenge', name: 'PracticeChallenge', component: () => import('@/views/practice/ChallengeView.vue') },
  { path: '/practice/project', name: 'PracticeProject', component: () => import('@/views/practice/ProjectView.vue') },
  // 社区
  { path: '/community/share', name: 'CommunityShare', component: () => import('@/views/community/Share.vue') },
  { path: '/community/forum', name: 'CommunityForum', component: () => import('@/views/community/Forum.vue') },
  { path: '/community/competition', name: 'CommunityCompetition', component: () => import('@/views/community/Competition.vue') },
  { path: '/community/competitioncenter',name:'CommunityCompetitionCenter', component: () => import('@/views/community/CompetitionCenter.vue')},
  // 用户中心
  { path: '/user/report', name: 'UserReport', component: () => import('@/views/user/Report.vue') },
  { path: '/user/profile', name: 'UserProfile', component: () => import('@/views/user/Profile.vue')},
  // 登录
  { path: '/login', component: LoginView },
  { path: '/set-password', component: SetPasswordView },
  // 404
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
