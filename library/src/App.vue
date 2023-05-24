<template>
  <div id="app">
    <header>
      <nav>
        <div class="nav-content">
          <h1>图书馆个性化服务系统</h1>
          <div class="user-button">
            <button v-if= 'isUsermanageRoute' @click="goToDashboard">回到首页</button>
            <button v-if= 'isDashboardRoute' @click="goToUserManagement">用户中心</button>
          </div>
        </div>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  computed: {
    isDashboardRoute() {
      return this.$route.name === 'Dashboard'; // 请根据您的路由配置来设置正确的路由名称
    },
    isUsermanageRoute() {
      return this.$route.name === 'Usermanage'; // 请根据您的路由配置来设置正确的路由名称
    }
  },
  data(){
    return {
    };
  },
  methods: {
    goToDashboard() {
      this.$router.push('/dashboard');
    },
    goToUserManagement() {
        this.$router.push('/usermanage');
    },
  },
  name: 'App'
};
</script>

<!-- 您可以在此处添加一些全局样式 -->
<style>
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
}

nav {
  background-color: #5c6bc0;
  padding: 5px;
}

h1 {
  margin: 0;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-button {
  margin-right: 20px;
}
.user-button button {
  font-size: 18px;
  background-color: transparent;
  color: #ffffff;
  font-weight: bold;
  border:1px solid transparent;
}
</style>
