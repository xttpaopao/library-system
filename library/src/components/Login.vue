<template>
  <div id="app">
    <div class="login">
      <form @submit.prevent="submitForm">
        <div class="form-row">
          <label for="username">用户名：</label>
          <input type="text" id="username" v-model="username" required/>
        </div>
        <div class="form-row">
          <label for="password">密 码：</label>
          <input type="password" id="password" v-model="password" required/>
        </div>
        <div>
          <button type="submit">登录</button>
        </div>
      </form>
      <div v-if="errorMessage">{{ errorMessage }}</div>
      <div>
        <p>还没有账户？
          <router-link to="/register">立即注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  created() {
    localStorage.setItem('userId', 0);
  },
  methods: {
    methods: {
      goToUserManagement() {
        this.$router.push('/usermanage');
      },
    },
    async submitForm() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          username: this.username,
          password: this.password
        });

        if (response.data.message === 'User Login successful') {
          setTimeout(() => {
            this.$message({
              message: "登录成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
            this.$router.push("/dashboard")
          }, 1000);
          localStorage.setItem('userId', response.data.userId);
          this.$store.commit('setIsAuthenticated', true);
        }
        if (response.data.message === 'Admin Login successful') {
          setTimeout(() => {
            this.$message({
              message: "登录成功,欢迎进入后台管理页面",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
            this.$router.push("/manage")
          }, 1000);
        }
      } catch (error) {
        if (error.response.status === 401) {
          this.errorMessage = '密码错误';
        } else if (error.response.status === 404) {
          this.errorMessage = '用户不存在';
        } else {
          this.errorMessage = '发生错误，请重试';
        }
      }
    }
  }
};
</script>

<style scoped>
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  background-image: url('./background.jpg');
  background-size: cover;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  width: 300px;
}

div {
  margin-bottom: 10px;
}

label {
  display: inline-block;
  margin-right: 10px;
}

button {
  background-color: #2196f3;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0d8bf2;
}


</style>


