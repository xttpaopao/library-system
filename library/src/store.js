import { createStore } from 'vuex';

const store = createStore({
    state: {
        userId: localStorage.getItem('userId') || null,
        isAuthenticated: false, // 新增 isAuthenticated 状态
    },
    mutations: {
        setUserId(state, userId) {
            state.userId = userId;
            localStorage.setItem('userId', userId);
        },
        setIsAuthenticated(state, isAuthenticated) { // 新增 setIsAuthenticated 变更方法
            state.isAuthenticated = isAuthenticated;
        },
    },
});

export default store;
