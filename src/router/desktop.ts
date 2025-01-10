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
    path: '/search',
    name: 'search',
    meta: {
      pageName: '兔兔趣味卡池中心'
    },
    component: () => import('@/desktop/views/SearchPool.vue')
  },
  {
    path: '/editor-home',
    name: 'editor-home',
    meta: {
      pageName: '卡池编辑'
    },
    component: () => import('@/desktop/views/EditorHome.vue'),
    children: [
      {
        path: '/edit-pool',
        name: 'edit-pool',
        meta: {
          pageName: '卡池编辑'
        },
        component: () => import('@/desktop/views/EditPool.vue'),
        children: [
        ]
      },      
      {
        path: '/edit-pool/edit-operator',
        name: 'edit-operator',
        meta: {
          pageName: '干员编辑'
        },
        component: () => import('@/desktop/views/EditOperator.vue'),
        children: [
        ]
      }
    ]
    
  }
]

export default desktopRoutes