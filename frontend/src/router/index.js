// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
// import Index from '../pages/index.vue'
// import Login from '../pages/login.vue'
// import About from '../views/About.vue'

const routes = [
  {
    path: '/',
    name: 'Index',
    component: () => import("@/pages/homeIndex.vue"),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import("@/pages/userLogin.vue"),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import("@/pages/userRegister.vue"),
  },
  {
    path: '/mainpage',
    name: 'MainPage',
    component: () => import("@/pages/mainPage/mainIndex.vue"),
    redirect: "/manage",
    meta: { requiresAuth: true},
    children: [
      {
        name: "manage",
        path: "/manage",
        component: () => import("@/pages/mainPage/manage.vue"),
      },
      {
        name: "analysis",
        path: "/analysis",
        component: () => import("@/pages/mainPage/analysis.vue"),
      },
      {
        name: "userManage",
        path: "/userManage",
        component: () => import("@/pages/mainPage/userManage.vue"),
      },
      {
        name: "history",
        path: "/history",
        component: () => import("@/pages/mainPage/history.vue"),
      },
      {
        name: "map",
        path: "/map",
        component: () => import("@/pages/mainPage/map.vue"),
      },
    ]
  },
  {
    path: '/userpage',
    name: 'userPage',
    component: () => import("@/pages/userPage/userIndex.vue"),
    redirect: "/datahub",
    meta: { requiresAuth: true},
    children: [
      {
        name: "datahub",
        path: "/datahub",
        component: () => import("@/pages/userPage/datahub.vue"),
      },
      {
        name: "uanalysis",
        path: "/uanalysis",
        component: () => import("@/pages/userPage/userAnalysis.vue"),
      },
      {
        name: "umap",
        path: "/umap",
        component: () => import("@/pages/userPage/userMap.vue"),
      },
     
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
router.beforeEach((next) => {
  next;
});

export default router
