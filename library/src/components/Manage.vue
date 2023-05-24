<template>
  <meta name="referrer" content="no-referrer"/>
  <div id="app">
    <div class="card-container" v-if="actcardVisibleAdd" @click="closeCard">
      <div class="card" @click.stop>
        <div class="input-container">
          <input type="text" placeholder="活动内容" v-model='content' class="custom-input"/>
          <el-date-picker v-model="publish_time" type="date" placeholder="publish_time" class="custom-input"
                          value-format="YYYY-MM-DD"></el-date-picker>
          <el-date-picker v-model="deadline_time" type="date" placeholder="deadline_time" class="custom-input"
                          value-format="YYYY-MM-DD"></el-date-picker>
          <button @click="ActAddConfirm()">submit</button>
        </div>
      </div>
    </div>
    <div class="card-container" v-if="commentcardVisible" @click="closeCard">
      <div class="card" @click.stop>
        <div class="input-container">
          <input type="text" placeholder="反馈回复" v-model='reply' class="custom-input"/>
          <button @click="commentReplyConfirm()">submit</button>
        </div>
      </div>
    </div>
    <div class="card-container" v-if="usercardVisibleAdd" @click="closeCard">
      <div class="card" @click.stop>
        <div class="input-container">
          <input type="text" placeholder="姓名" v-model='username' class="custom-input"/>
          <input type="text" placeholder="邮箱" v-model='email' class="custom-input"/>
          <input type="text" placeholder="密码" v-model='password' class="custom-input"/>
          <button @click="UserAddConfirm()">submit</button>
        </div>
      </div>
    </div>
    <div class="card-container" v-if="usercardVisibleModify" @click="closeCard">
      <div class="card" @click.stop>
        <div class="input-container">
          <input type="text" placeholder="姓名" v-model='username' class="custom-input"/>
          <input type="text" placeholder="邮箱" v-model='email' class="custom-input"/>
          <input type="text" placeholder="密码" v-model='password' class="custom-input"/>
          <input type="text" placeholder="管理员（0或1）" v-model='is_admin' class="custom-input"/>
          <button @click="UserModifyConfirm">submit</button>
        </div>
      </div>
    </div>
    <div class="card-container" v-if="bookcardVisibleAdd" @click="closeCard">
      <div class="card" @click.stop>
        <div class="input-container">
          <input type="text" placeholder="title" v-model='title' class="custom-input"/>
          <input type="text" placeholder="author" v-model='author' class="custom-input"/>
          <input type="text" placeholder="isbn" v-model='isbn' class="custom-input"/>
          <input type="text" placeholder="description" v-model='description' class="custom-input"/>
          <input type="text" placeholder="category" v-model='category' class="custom-input"/>
          <input type="text" placeholder="tags" v-model='tags' class="custom-input"/>
          <input type="text" placeholder="cover" v-model='cover' class="custom-input"/>
          <button @click="BookAddConfirm">submit</button>
        </div>
      </div>
    </div>
    <div class="card-container" v-if="bookcardVisibleModify" @click="closeCard">
      <div class="card" @click.stop>
        <div class="input-container">
          <input type="text" placeholder="title" v-model='title' class="custom-input"/>
          <input type="text" placeholder="author" v-model='author' class="custom-input"/>
          <input type="text" placeholder="isbn" v-model='isbn' class="custom-input"/>
          <input type="text" placeholder="description" v-model='description' class="custom-input"/>
          <input type="text" placeholder="category" v-model='category' class="custom-input"/>
          <input type="text" placeholder="tags" v-model='tags' class="custom-input"/>
          <input type="text" placeholder="cover" v-model='cover' class="custom-input"/>
          <button @click="BookModifyConfirm">submit</button>
        </div>
      </div>
    </div>
    <div class="card-container" v-if="borrowcardVisibleAdd" @click="closeCard">
      <div class="card" @click.stop>
        <div class="input-container">
          <input type="text" placeholder="user_id" v-model='user_id' class="custom-input"/>
          <input type="text" placeholder="book_id" v-model='book_id' class="custom-input"/>
          <el-date-picker v-model="borrow_date" type="date" placeholder="borrow_date" class="custom-input"
                          value-format="YYYY-MM-DD"></el-date-picker>
          <el-date-picker v-model="return_date" type="date" placeholder="return_date" class="custom-input"
                          value-format="YYYY-MM-DD"></el-date-picker>
          <el-date-picker v-model="due_date" type="date" placeholder="due_date" class="custom-input"
                          value-format="YYYY-MM-DD"></el-date-picker>
          <button @click="BorrowAddConfirm">submit</button>
        </div>
      </div>
    </div>
    <div class="card-container" v-if="borrowcardVisibleModify" @click="closeCard">
      <div class="card" @click.stop>
        <div class="input-container">
          <input type="text" placeholder="user_id" v-model='user_id' class="custom-input"/>
          <input type="text" placeholder="book_id" v-model='book_id' class="custom-input"/>
          <el-date-picker v-model="borrow_date" type="date" placeholder="borrow_date" class="custom-input"
                          value-format="YYYY-MM-DD"></el-date-picker>
          <el-date-picker v-model="return_date" type="date" placeholder="return_date" class="custom-input"
                          value-format="YYYY-MM-DD"></el-date-picker>
          <el-date-picker v-model="due_date" type="date" placeholder="due_date" class="custom-input"
                          value-format="YYYY-MM-DD"></el-date-picker>
          <button @click="BorrowModifyConfirm">submit</button>
        </div>
      </div>
    </div>
    <div id="manage">
      <div class="sidebar">
        <button
            :class="{ active: currentView === 'dashboard' }"
            @click="currentView = 'dashboard'"
        >
          首页
        </button>
        <button
            :class="{ active: currentView === 'userManagement' }"
            @click="currentView = 'userManagement';fetchUsers()"
        >
          用户管理
        </button>
        <button
            :class="{ active: currentView === 'borrowManagement' }"
            @click="currentView = 'borrowManagement';fetchBorrows()"
        >
          借阅管理
        </button>
        <button
            :class="{ active: currentView === 'bookManagement' }"
            @click="currentView = 'bookManagement';fetchBooks()"
        >
          图书管理
        </button>
        <button
            :class="{ active: currentView === 'commentManagement' }"
            @click="currentView = 'commentManagement'"
        >
          评价反馈
        </button>
      </div>

      <div class="content">
        <div v-if="currentView === 'dashboard'">
          <!-- 首页内容 -->
          <h2>首页</h2>
          <h2>活动发布</h2>
          <table class="user-table">
            <thead>
            <tr>
              <th>activities</th>
              <th>publish_time</th>
              <th>deadline_time</th>
              <th>
                <button @click="addAct()" class="add-button">添加</button>
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="book in activities" :key="book[0]">
              <td>{{ book[1] }}</td>
              <td>{{ book[2] }}</td>
              <td>{{ book[3] }}</td>
              <td></td>
            </tr>
            </tbody>
          </table>
          <h2>热门推荐</h2>
          <table class="user-table">
            <thead>
            <tr>
              <th>id</th>
              <th>title</th>
              <th>author</th>
              <th>isbn</th>
              <th>description</th>
              <th>category</th>
              <th>tags</th>
              <th>cover</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="book in hotbooks" :key="book[0]">
              <td>{{ book[0] }}</td>
              <td>{{ book[1] }}</td>
              <td>{{ book[2] }}</td>
              <td>{{ book[3] }}</td>
              <td>{{ book[4] }}</td>
              <td>{{ book[5] }}</td>
              <td>{{ book[6] }}</td>
              <td><img :src="book[7]"></td>
            </tr>
            </tbody>
          </table>
        </div>
        <div v-if="currentView === 'userManagement'">
          <!-- 用户管理内容 -->
          <h2>用户管理</h2>
          <table class="user-table">
            <thead>
            <tr>
              <th>id</th>
              <th>姓名</th>
              <th>邮箱</th>
              <th>密码</th>
              <th>管理员</th>
              <th>推荐书籍</th>
              <th>
                <button @click="addUser()" class="add-button">添加</button>
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="user in users" :key="user[0]">
              <td>{{ user[0] }}</td>
              <td>{{ user[1] }}</td>
              <td>{{ user[2] }}</td>
              <td>{{ user[3] }}</td>
              <td>{{ user[4] }}</td>
              <td>{{ user[5] }}</td>
              <td>
                <button @click="modifyUser(user[0])" class="modify-button">修改</button>
                <button @click="deleteUser(user[0])" class="delete-button">删除</button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
        <div v-if="currentView === 'borrowManagement'">
          <!-- 借阅管理内容 -->
          <h2>借阅管理</h2>
          <table class="user-table">
            <thead>
            <tr>
              <th>borrow_id</th>
              <th>user_id</th>
              <th>book_id</th>
              <th>borrow_date</th>
              <th>return_date</th>
              <th>due_date</th>
              <th>
                <button @click="addBorrow()" class="add-button">添加</button>
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="borrow in borrows" :key="borrow[0]">
              <td>{{ borrow[0] }}</td>
              <td>{{ borrow[1] }}</td>
              <td>{{ borrow[2] }}</td>
              <td>{{ borrow[3] }}</td>
              <td>{{ borrow[4] }}</td>
              <td>{{ borrow[5] }}</td>
              <td>
                <button @click="modifyBorrow(borrow[0])" class="modify-button">修改</button>
                <button @click="deleteBorrow(borrow[0])" class="delete-button">删除</button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
        <div v-if="currentView === 'bookManagement'">
          <!-- 图书管理内容 -->
          <h2>图书管理</h2>
          <table class="user-table">
            <thead>
            <tr>
              <th>id</th>
              <th>title</th>
              <th>author</th>
              <th>isbn</th>
              <th>description</th>
              <th>category</th>
              <th>tags</th>
              <th>剩余本数</th>
              <th>用户评价</th>
              <th>
                <button @click="addBook()" class="add-button">添加</button>
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="book in books" :key="book[0]">
              <td>{{ book[0] }}</td>
              <td>{{ book[1] }}</td>
              <td>{{ book[2] }}</td>
              <td>{{ book[3] }}</td>
              <td>{{ book[4] }}</td>
              <td>{{ book[5] }}</td>
              <td>{{ book[6] }}</td>
              <td>{{ book[8] }}</td>
              <td>{{ book[9] }}</td>
              <td>
                <button @click="modifyBook(book[0])" class="modify-button">修改</button>
                <button @click="deleteBook(book[0])" class="delete-button">删除</button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
        <div v-if="currentView === 'commentManagement'">
          <!-- 图书管理内容 -->
          <h3>来自用户的建议</h3>
          <table class="user-table">
            <thead>
            <tr>
              <th>user_id</th>
              <th>comment</th>
              <th></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="comment in comments_sys" :key="comment[-1]">
              <td>{{ comment[0] }}</td>
              <td>{{ comment[1] }}</td>
              <td>
                <button @click="commentReply(comment[0])" class="modify-button">回复</button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      content: '',
      publish_time: '',
      deadline_time: '',
      reply: '',
      borrowId: 0,
      bookId: 0,
      userId: 0,
      username: '',
      email: '',
      password: '',
      is_admin: '',
      title: '',
      author: '',
      isbn: '',
      description: '',
      category: '',
      tags: '',
      cover: '',
      user_id: '',
      book_id: '',
      borrow_date: '',
      return_date: '',
      due_date: '',
      commentcardVisible: false,
      usercardVisibleAdd: false,
      usercardVisibleModify: false,
      bookcardVisibleAdd: false,
      bookcardVisibleModify: false,
      borrowcardVisibleAdd: false,
      borrowcardVisibleModify: false,
      actcardVisibleAdd: false,
      currentView: 'dashboard',
      users: [],
      books: [],
      borrows: [],
      comments_books: [],
      comments_sys: [],
      hotbooks: [],
      activities: []
    };
  },
  methods: {
    commentReply(userId) {
      this.commentcardVisible = true;
      this.userId = userId;
    },
    addUser() {
      this.usercardVisibleAdd = true;
    },
    addAct() {
      this.actcardVisibleAdd = true;
    },
    addBook() {
      this.bookcardVisibleAdd = true;
    },
    addBorrow() {
      this.borrowcardVisibleAdd = true;
    },
    async UserAddConfirm() {
      try {
        const response = await axios.post('http://localhost:5000/register', {
          username: this.username,
          email: this.email,
          password: this.password
        });

        if (response.data.message === '注册成功') {
          setTimeout(() => {
            this.$message({
              message: "添加成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "添加失败",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      } catch (error) {
        if (error.response.status === 400) {
          setTimeout(() => {
            this.$message({
              message: "用户已存在",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "发生错误，请重试",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    async ActAddConfirm() {
      try {
        const response = await axios.post('http://localhost:5000/activities', {
          content: this.content,
          publish_time: this.publish_time,
          deadline_time: this.deadline_time
        });

        if (response.data.message === 'activity published successfully') {
          setTimeout(() => {
            this.$message({
              message: "活动发布成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "失败",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      } catch (error) {
        if (error.response.status === 400) {
          setTimeout(() => {
            this.$message({
              message: "something wrong happened",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "发生错误，请重试",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    async BookAddConfirm() {
      try {
        const response = await axios.post('http://localhost:5000/books', {
          title: this.title,
          author: this.author,
          isbn: this.isbn,
          description: this.description,
          category: this.category,
          tags: this.tags,
          cover: this.cover
        });

        if (response.data.message === 'Book created successfully') {
          setTimeout(() => {
            this.$message({
              message: "添加成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "添加失败",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      } catch (error) {
        if (error.response.status === 400) {
          setTimeout(() => {
            this.$message({
              message: "图书已存在",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "发生错误，请重试",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    async BorrowAddConfirm() {
      try {
        const response = await axios.post('http://localhost:5000/borrow_records', {
          user_id: this.user_id,
          book_id: this.book_id,
          borrow_date: this.borrow_date,
          return_date: this.return_date,
          due_date: this.due_date
        });

        if (response.data.message === 'Borrow record created successfully') {
          setTimeout(() => {
            this.$message({
              message: "添加成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "添加失败",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      } catch (error) {
        if (error.response.status === 400) {
          setTimeout(() => {
            this.$message({
              message: "Someting wrong",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "发生错误，请重试",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    closeCard() {
      this.commentcardVisible = false;
      this.usercardVisibleAdd = false;
      this.usercardVisibleModify = false;
      this.bookcardVisibleModify = false;
      this.bookcardVisibleAdd = false;
      this.borrowcardVisibleModify = false;
      this.borrowcardVisibleAdd = false;
    },

    fetchUsers() {
      axios.get('http://localhost:5000/users').then((response) => {
        this.users = response.data;
      });
    },
    fetchBooks() {
      axios.get('http://localhost:5000/books').then((response) => {
        this.books = response.data;
      });
      axios.get('http://localhost:5000/comments_books').then((response) => {
        this.comments_books = response.data;
      });
    },
    fetchBorrows() {
      axios.get('http://localhost:5000/borrows').then((response) => {
        this.borrows = response.data;
      });
    },
    modifyUser(userId) {
      this.usercardVisibleModify = true;
      this.userId = userId;
    },
    modifyBook(bookId) {
      this.bookcardVisibleModify = true;
      this.bookId = bookId;
    },
    modifyBorrow(borrowId) {
      this.borrowcardVisibleModify = true;
      this.borrowId = borrowId;
    },
    async commentReplyConfirm() {
      try {
        const response = await axios.put(`http://localhost:5000/reply/${this.userId}`, {
          'reply': this.reply
        });

        if (response.data.message === 'User updated successfully') {
          setTimeout(() => {
            this.$message({
              message: "回复成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {

        }
      } catch (error) {
        if (error.response.status === 400) {
          setTimeout(() => {
            this.$message({
              message: "Missing Fields",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "error code 500",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    async UserModifyConfirm() {
      try {
        const response = await axios.put(`http://localhost:5000/users/${this.userId}`, {
          username: this.username,
          email: this.email,
          password: this.password,
          is_admin: this.is_admin
        });

        if (response.data.message === 'User updated successfully') {
          setTimeout(() => {
            this.$message({
              message: "修改成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {

        }
      } catch (error) {
        if (error.response.status === 400) {
          setTimeout(() => {
            this.$message({
              message: "Missing Fields",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "error code 500",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    async BookModifyConfirm() {
      try {
        const response = await axios.put(`http://localhost:5000/books/${this.bookId}`, {
          title: this.title,
          author: this.author,
          isbn: this.isbn,
          description: this.description,
          category: this.category,
          tags: this.tags,
          cover: this.cover
        });

        if (response.data.message === 'Book updated successfully') {
          setTimeout(() => {
            this.$message({
              message: "修改成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {

        }
      } catch (error) {
        if (error.response.status === 400) {
          setTimeout(() => {
            this.$message({
              message: "Missing Fields",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "error code 500",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    async BorrowModifyConfirm() {
      try {
        const response = await axios.put(`http://localhost:5000/borrow_records/${this.borrowId}`, {
          user_id: this.user_id,
          book_id: this.book_id,
          borrow_date: this.borrow_date,
          return_date: this.return_date,
          due_date: this.due_date
        });

        if (response.data.message === 'Borrow record updated successfully') {
          setTimeout(() => {
            this.$message({
              message: "修改成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {

        }
      } catch (error) {
        if (error.response.status === 400) {
          setTimeout(() => {
            this.$message({
              message: "Missing Fields",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "error code 500",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    async deleteBook(bookId) {
      try {
        const response = await axios.delete(`http://localhost:5000/books/${bookId}`);
        if (response.data.message === 'Book deleted successfully') {
          setTimeout(() => {
            this.$message({
              message: "删除成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {

        }
      } catch (error) {
        if (error.response.status === 404) {
          setTimeout(() => {
            this.$message({
              message: "Book not found",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "由于存在借阅记录，无法删除",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    async deleteUser(userId) {
      try {
        const response = await axios.delete(`http://localhost:5000/users/${userId}`);
        if (response.data.message === 'User deleted successfully') {
          setTimeout(() => {
            this.$message({
              message: "删除成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {

        }
      } catch (error) {
        if (error.response.status === 404) {
          setTimeout(() => {
            this.$message({
              message: "User not found",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "error code 500",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
    async deleteBorrow(borrowId) {
      try {
        const response = await axios.delete(`http://localhost:5000/borrow_records/${borrowId}`);
        if (response.data.message === 'Borrow record deleted successfully') {
          setTimeout(() => {
            this.$message({
              message: "删除成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {

        }
      } catch (error) {
        if (error.response.status === 404) {
          setTimeout(() => {
            this.$message({
              message: "record not found",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "error code 500",
              type: "error", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      }
    },
  },
  created() {
    axios.get('http://localhost:5000/comments_sys').then((response) => {
      this.comments_sys = response.data;
    });
    axios.get('http://localhost:5000/api/hotBooks').then((response) => {
      this.hotbooks = response.data;
    });
    axios.get("http://localhost:5000/activities").then((response) => {
      this.activities = response.data;
    });
  },
};
</script>

<style>
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#manage {
  height: 640px;
  display: flex;
  min-height: 94.4vh;
  position: relative;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  background-color: #5c6bc0;
  min-width: 160px;
}

.sidebar button {
  background-color: transparent;
  border: none;
  border-radius: 15px;
  padding: 10px;
  color: white;
  cursor: pointer;
  text-align: left;
  outline: none;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.sidebar button.active,
.sidebar button:hover {
  background-color: #3f51b5;
}

.content {
  flex-grow: 1;
  padding: 20px;
  height: 650px;
  overflow-y: auto;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  overflow: hidden;
  position: relative;
}

.user-table thead {
  position: sticky;
  top: 0;
  background-color: #fff;
}

.user-table th,
.user-table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: left;
}
.user-table td img {
  height: 150px;
  object-fit: contain;
}

.modify-button {
  background-color: #3f51b5;
  color: #fff;
  border-radius: 5px;
  margin-right: 5px;
}

.delete-button {
  background-color: #f44336;
  border-radius: 5px;
  color: #fff;
}

.add-button {
  background-color: #3f51b5;
  border-radius: 5px;
  color: #fff;
}

.card-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.card {
  background-color: white;
  width: 400px; /* 调整卡片的宽度 */
  max-width: 90%; /* 设置最大宽度，以避免在小屏幕上溢出 */
  padding: 20px; /* 内边距，可以根据需要调整 */
  border-radius: 10px; /* 圆角边框 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  display: flex;
}

.input-container {
  display: flex;
  flex-direction: column;
}

.custom-input {
  margin-bottom: 20px;
  border-radius: 15px;
  width: 380px; /* 修改输入框宽度 */
  height: 40px; /* 修改输入框高度 */
  padding: 0 10px; /* 增加左右内边距以获得更好的视觉效果 */
}

.log {
  background-color: #f8f9fa;
  border-radius: 5px;
  padding: 20px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin-bottom: 10px;
}
</style>
