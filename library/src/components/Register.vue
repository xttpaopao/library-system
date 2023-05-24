<template>
  <div class="register">
    <h1>注册账户</h1>
    <form @submit.prevent="submitForm">
      <div class="form-row">
        <label for="username">用户名：</label>
        <input type="text" id="username" v-model="username" required/>
      </div>
      <div class="form-row">
        <label for="email">邮箱：</label>
        <input type="text" id="email" v-model="email" required/>
      </div>
      <div class="form-row">
        <label for="password">密码：</label>
        <input type="password" id="password" v-model="password" required/>
      </div>
      <div class="form-row">
        <label for="confirmPassword">确认密码：</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required/>
      </div>
      <div>
        <button type="submit">注册</button>
      </div>
    </form>
    <div v-if="errorMessage">{{ errorMessage }}</div>
    <div>
      <p>已有账户？
        <router-link to="/">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      errorMessage: ''
    };
  },
  methods: {
    async submitForm() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = '两次密码输入不一致';
        return;
      }

      try {
        const response = await axios.post('http://localhost:5000/register', {
          username: this.username,
          email: this.email,
          password: this.password
        });

        if (response.data.message === '注册成功') {
          this.$router.push('/');
        } else {
          this.errorMessage = '注册失败';
        }
      } catch (error) {
        if (error.response.status === 400) {
          this.errorMessage = '用户名已存在';
        } else {
          this.errorMessage = '发生错误，请重试';
        }
      }
    }
  }
};
</script>

<style scoped>
.register {
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
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

label {
  margin-right: 10px;
  text-align: right;
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

.errorMessage {
  margin-top: 10px;
  color: #f44336;
}
</style>
