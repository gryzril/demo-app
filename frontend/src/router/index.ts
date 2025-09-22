import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

const Login = () => import('@/views/Login.vue');
const Dashboard = () => import('@/views/Dashboard.vue');

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;