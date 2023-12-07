import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/userStore'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')

const userStore = useUserStore()

router.beforeEach((to, from, next) => {
    if (to.meta.requireAuth) {
        if (userStore.user.token) {
            next()
        } else {
            next({ name: 'login' })
        }
    } else {
        next()
    }
    
})