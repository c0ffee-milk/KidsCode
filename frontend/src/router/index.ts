import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import MineView from '@/views/MineView.vue'
import LearnView from '@/views/LearnView.vue'

const routes = [
  { path: '/', component: HomeView },
  {
    path: '/login',
    component: LoginView,
  },
  {
    path: '/register',
    component: RegisterView,
  },
  {
    path: '/learn',
    name: 'Learn',
    component: LearnView
  },
  {
    path: '/mine',
    component: MineView,
  },
  {
    path: '/:pathMatch(.*)*',
    component: NotFoundView,
  }
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
