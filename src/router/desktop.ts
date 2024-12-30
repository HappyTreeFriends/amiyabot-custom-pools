import type { RouteRecordRaw } from 'vue-router'
//import EmptyContainer from '@/desktop/components/EmptyContainer.vue'

const desktopRoutes: RouteRecordRaw[] = [
  {
    path: '/home',
    name: 'home',
    meta: {
      pageName: '兔兔趣味卡池中心'
    },
    component: () => import('@/desktop/views/Home.vue')
  },
  {
    path: '/edit-pool',
    name: 'edit-pool',
    meta: {
      pageName: '编辑卡池'
    },
    component: () => import('@/desktop/views/EditPool.vue')
  }
]

export default desktopRoutes