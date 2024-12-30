import { createRouter, createWebHashHistory } from 'vue-router'
import desktopRoutes from '@/router/desktop'
//import mobileRoutes from '@/router/mobile'

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        ...desktopRoutes,
        //...mobileRoutes
    ]
})

router.beforeEach((to, _from, next) => {

    //移动端强制跳转
    if (window.innerWidth < 768 && to.path.startsWith('/m/') === false) {
        next(`/m${to.path}`)
        return
    }
    if (window.innerWidth >= 768 && to.path.startsWith('/m/') === true) {
        next(to.path.replace('/m/', '/'))
        return
    }


    if (to.path !== '/' && to.path !== '/home' && to.path !== '/m/' && to.path !== '/m/home') {
        next()
        return
    }

    if (to.path === '/') {
        next('/home')
        return
    }

    if (to.path === '/m/') {
        next('/m/home')
        return
    }

    next()
})

export default router