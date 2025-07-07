import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import MineView from '@/views/MineView.vue'
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
    path: '/:pathMatch(.*)*',
    component: NotFoundView,
  },
  {
    path: '/mine',
    component: MineView,
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
