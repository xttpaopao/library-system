import {createRouter, createWebHistory} from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import Login from '../components/Login.vue';
import store from "@/store";
import Register from "@/components/Register.vue";
import Manage from "@/components/Manage.vue";
import Usermanage from "@/components/Usermanage.vue";

const routes = [
    {
        path: '/usermanage',
        name: 'Usermanage',
        component: Usermanage,
        meta: {
            requiresAuth: true,
        },
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: {
            requiresAuth: true,
        },
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
    {
        path: '/',
        name: 'Login',
        component: Login,
    },
    {
        path: '/register',
        name: 'register',
        component: Register,
    },
    {
        path: '/manage',
        name: 'manage',
        component: Manage,
        meta: {
            requiresAuth: true,
        },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const userId = localStorage.getItem('userId');
    store.commit('setUserId', userId);
    const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
    const isAuthenticated = store.state.userId !== null;

    if (requiresAuth && !isAuthenticated) {
        next('/');
    } else {
        next();
    }
});

export default router;
