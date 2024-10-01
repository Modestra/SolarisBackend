import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../views/MainPage.vue'
import AuthorizationPage from '../views/AuthorizationPage.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {
            path: '/',
            name: 'home',
            component: MainPage
        },
        {
            path: '/AuthorizationPage',
            name: 'AuthorizationPage',
            component: AuthorizationPage
        },
    ]
})

export default router