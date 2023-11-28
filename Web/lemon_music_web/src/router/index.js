import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/dashboard/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/dashboard',
      name: 'dashboard',
      component: HomeView
    },
    {
      path: '/music_lib',
      name: 'home',
      component: HomeView
    }
  ]
})

export default router
