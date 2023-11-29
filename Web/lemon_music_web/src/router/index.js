import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/dashboard/DashboardView.vue'
import MusicLibView from '../views/dashboard/MusicLibView.vue'
import HomeView from '../views/dashboard/HomeView.vue'
import LoginView from '../views/dashboard/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView,
      children: [
        {
          path: '/dashboard',
          name: 'dashboard',
          component: DashboardView
        },
        {
          path: '/music_lib',
          name: 'home',
          component: MusicLibView
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView      
    }
  ]
})

export default router
