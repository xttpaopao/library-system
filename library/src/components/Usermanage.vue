<template>
  <meta name="referrer" content="no-referrer"/>
  <div id="app">
    <div class="card-container" v-if="cardVisible" @click="closeCard">
      <div class="card" @click.stop>
        <img :src="selectedBook[4][0][4]" alt="book cover" class="card-cover">
        <div class="book-info">
          <h4>书名：{{ selectedBook[4][0][0] }}</h4>
          <p>&nbsp;</p>
          <p>作者：{{ selectedBook[4][0][1] }}</p>
          <p>分类：{{ selectedBook[4][0][3] }}</p>
          <p>描述：{{ selectedBook[4][0][2] }}</p>
          <p>剩余：{{ selectedBook[4][0][5] }}本</p>
          <p>&nbsp;</p>
          <button class="borrow-btn" @click="continueborrow(selectedBook[0])"
                  :class="{ 'button-disabled': continueborrowed }"
                  :disabled="continueborrowed">{{ continueborrowed ? '续借成功' : '续借' }}
          </button>
          <button class="borrow-btn" @click="returnBook(selectedBook[0])">还书</button>
        </div>
      </div>
    </div>
    <div class="card-container" v-if="cardVisiblereserved" @click="closeCard">
      <div class="card" @click.stop>
        <img :src="selectedreservedBook[3][0][4]" alt="book cover" class="card-cover">
        <div class="book-info">
          <h4>书名：{{ selectedreservedBook[3][0][0] }}</h4>
          <p>&nbsp;</p>
          <p>作者：{{ selectedreservedBook[3][0][1] }}</p>
          <p>分类：{{ selectedreservedBook[3][0][3] }}</p>
          <p>描述：{{ selectedreservedBook[3][0][2] }}</p>
          <p>&nbsp;</p>
          <p>剩余：{{ selectedreservedBook[3][0][5] }}本</p>
          <p>&nbsp;</p>
          <button class="borrow-btn" v-if="reservedBorrowVisable" @click="borrowBook(selectedreservedBook[2])">借阅
          </button>
        </div>
      </div>
    </div>
    <div class="card-container" v-if="cardVisibleliked" @click="closeCard">
      <div class="card" @click.stop>
        <img :src="selectedlikedBook[7]" alt="book cover" class="card-cover">
        <div class="book-info">
          <h4>书名：{{ selectedlikedBook[1] }}</h4>
          <p>&nbsp;</p>
          <p>作者：{{ selectedlikedBook[2] }}</p>
          <p>ISBN：{{ selectedlikedBook[3] }}</p>
          <p>分类：{{ selectedlikedBook[5] }}</p>
          <p>标签：{{ selectedlikedBook[6] }}</p>
          <p>描述：{{ selectedlikedBook[4] }}</p>
          <p>&nbsp;</p>
          <p>剩余：{{ selectedlikedBook[8] }}本</p>
          <p>&nbsp;</p>
          <button class="borrow-btn" v-if="likedBorrowVisable" @click="borrowBook(selectedlikedBook[0])">借阅</button>
        </div>
      </div>
    </div>
    <div class="user-profile">
      <div class="sidebar">
        <button
            :class="{ active: currentView === 'userManagement' }"
            @click="currentView = 'userManagement';clearMessages()"
        >
          个人信息
        </button>
        <button
            :class="{ active: currentView === 'messegeManagement' }"
            @click="currentView = 'messegeManagement';updateMessages()"
        >
          消 息
        </button>
        <button
            :class="{ active: currentView === 'borrowManagement' }"
            @click="currentView = 'borrowManagement';fetchBorrowedBooks();fetchReservedBooks();fetchLikedBooks();clearMessages()"
        >
          借阅管理
        </button>
      </div>
      <div class="content">
        <div v-if="currentView === 'userManagement'">
          <div class="messegeform">
            <h1>个人资料</h1>
            <form @submit.prevent="">
              <div class="form-group">
                <label for="name">name</label>
                <input type="text" id="name" v-model="username"/>
              </div>
              <div class="form-group">
                <label for="email">email</label>
                <input type="email" id="email" v-model="email"/>
              </div>
              <div class="form-group">
                <label for="password">password</label>
                <input type="password" id="password" v-model="password"/>
              </div>
              <button type="submit" @click="updateUserProfile">更新个人资料</button>
            </form>
          </div>
        </div>
        <div v-if="currentView === 'borrowManagement'">
          <div class="filtered">
            <h3>已经借阅的书籍</h3>
            <div class="book-list">
              <div class="book" v-for="book in borrowedBooks" :key="book[0]" @click="showBookDetails(book)">
                <img :src="book[4][0][4]" alt="book cover"/>
                <div class="book-info">
                  <h4>{{ book[4][0][0] }}</h4>
                  <p>{{ book[4][0][1] }}</p>
                  <p>借阅时间:{{ book[2] }}</p>
                  <p>借阅期限:{{ book[3] }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="filtered">
            <h3>已经预约的书籍</h3>
            <div class="book-list">
              <div class="book" v-for="book in reservedBooks" :key="book[2]" @click="showreservedBookDetails(book)">
                <img :src="book[3][0][4]" alt="book cover"/>
                <div class="book-info">
                  <h4>{{ book[3][0][0] }}</h4>
                  <p>{{ book[3][0][1] }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="filtered" v-if="recommendVisable">
            <h3>猜你想看</h3>
            <div class="book-list">
              <div class="book" v-for="book in likedBooks" :key="book[0]" @click="showlikedBookDetails(book)">
                <img :src="book[7]" alt="book cover"/>
                <div class="book-info">
                  <h4>{{ book[1] }}</h4>
                  <p>{{ book[2] }}</p>
                  <p>剩余:{{ book[8] }}本</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="currentView === 'messegeManagement'">
          <div class="message-list">
            <div v-for="(message, index) in messages" :key="index" class="message-box">
              <p class="message-content">{{ message }}</p>
              <button class="delete-btn" @click="removeMessage(index)">×</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import store from "@/store";

export default {
  data() {
    return {
      userId: 0,
      content: [],
      messages: [],
      userreview: '希望能加入更多的书本',
      adminreply: '收到您的评价，我们已经在购入新的书籍',
      currentView: 'userManagement',
      username: null,
      email: null,
      password: null,
      profile: [],
      borrowedBooks: [],
      reservedBooks: [],
      selectedBook: [],
      selectedlikedBook: [],
      selectedreservedBook: [],
      likedBooks: [],
      cardVisible: false,
      cardVisibleliked: false,
      cardVisiblereserved: false,
      recommendVisable: false,
      continueborrowed: false,
      reservedBorrowVisable: true,
      likedBorrowVisable: true,
    };
  },
  created() {
    const userId = store.state.userId;
    axios.get(`http://localhost:5000/profile/messege/${userId}`).then((response) => {
      this.content = response.data;
    });
    this.userId = userId;
    axios.get(`http://localhost:5000/user/${userId}`).then((response) => {
      this.profile = response.data;
      this.username = this.profile[0]
      this.email = this.profile[1]
      this.password = this.profile[2]
      if (response.status === 200) {
        this.recommendVisable = true;
      }
    });
    this.updateMessages();
  },
  methods: {
    async borrowBook(book_id) {
      // 获取用户ID和书籍ID
      const userId = store.state.userId;
      // 创建请求的数据对象
      const requestData = {
        userId: userId,
        bookId: book_id,
      };

      try {
        // 发送POST请求到后端的借阅接口
        const response = await axios
            .post("http://localhost:5000/api/borrow", requestData)
            .catch((error) => {
              console.error("Error fetching search results:", error);
            });

        // 检查请求是否成功
        if (response.data.message === "Borrow record added successfully!") {
          setTimeout(() => {
            this.$message({
              message: "借阅成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
          this.borrowed = true;
          // 在这里处理成功借阅的逻辑，例如关闭卡片，显示提示等
        } else {
          setTimeout(() => {
            this.$message({
              message: "failed",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      } catch (error) {
        setTimeout(() => {
          this.$message({
            message: "error",
            type: "error", // 消息类型，可选值有：success / warning / info / error
            duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
          });
        }, 1000);
      }
    },
    closeCard() {
      this.cardVisible = false;
      this.cardVisibleliked = false;
      this.cardVisiblereserved = false;
    },
    showlikedBookDetails(book) {
      this.selectedlikedBook = book;
      this.cardVisibleliked = true;
      if (this.selectedlikedBook[8] === 0) {
        this.likedBorrowVisable = false;
      } else {
        this.likedBorrowVisable = true;
      }
    },
    showreservedBookDetails(book) {
      this.selectedreservedBook = book;
      this.cardVisiblereserved = true;
      if (this.selectedreservedBook[3][0][5] === 0) {
        this.reservedBorrowVisable = false;
      } else {
        this.reservedBorrowVisable = true;
      }

    },
    showBookDetails(book) {
      this.selectedBook = book;
      this.cardVisible = true;
    },
    async returnBook(borrow_id) {
      try {
        // 发送POST请求到后端的借阅接口
        const response = await axios
            .put(`http://localhost:5000/profile/return/${borrow_id}`)
            .catch((error) => {
              console.error("Error fetching search results:", error);
            });

        // 检查请求是否成功
        if (response.data.message === "return successfully") {
          setTimeout(() => {
            this.$message({
              message: "还书成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        } else {
          setTimeout(() => {
            this.$message({
              message: "failed",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      } catch (error) {
        setTimeout(() => {
          this.$message({
            message: "error",
            type: "error", // 消息类型，可选值有：success / warning / info / error
            duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
          });
        }, 1000);
      }
    },
    async continueborrow(borrow_id) {
      try {
        // 发送POST请求到后端的借阅接口
        const response = await axios
            .put(`http://localhost:5000/profile/continueborrow/${borrow_id}`)
            .catch((error) => {
              console.error("Error fetching search results:", error);
            });

        // 检查请求是否成功
        if (response.data.message === "Due date extended successfully") {
          setTimeout(() => {
            this.$message({
              message: "续借成功",
              type: "success", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
          this.continueborrowed = true;
        } else {
          setTimeout(() => {
            this.$message({
              message: "failed",
              type: "warning", // 消息类型，可选值有：success / warning / info / error
              duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
            });
          }, 1000);
        }
      } catch (error) {
        setTimeout(() => {
          this.$message({
            message: "error",
            type: "error", // 消息类型，可选值有：success / warning / info / error
            duration: 3000, // 设置消息提示框自动关闭的时间，单位为毫秒
          });
        }, 1000);
      }
    },
    async fetchLikedBooks() {
      axios.get(`http://localhost:5000/api/likedBooks/${this.userId}`).then((response) => {
        this.likedBooks = response.data;
        if (response.status === 200) {
          this.recommendVisable = true;
        }
      });
    },
    async fetchReservedBooks() {
      const response = await axios.get(`http://localhost:5000/profile/reserved/${this.userId}`);
      this.reservedBooks = response.data
    },
    async fetchBorrowedBooks() {
      const response = await axios.get(`http://localhost:5000/profile/borrowed/${this.userId}`);
      this.borrowedBooks = response.data
    },
    async updateUserProfile() {
      try {
        const response = await axios.put(`http://localhost:5000/users/${this.userId}`, {
          'username': this.username,
          'email': this.email,
          'password': this.password
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
    updateMessages() {
      this.content.forEach(message => {
        this.messages.unshift(`New message: ${message}`);
      });
    },
    removeMessage(index) {
      this.messages.splice(index, 1);
    },
    clearMessages() {
      this.messages.length = 0;
    },
  },
};
</script>

<style scoped>
.user-profile {
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
  overflow-y: auto;
  display: flex;
  position: relative;
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

.form-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  width: 300px;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message-box {
  display: flex;
  width: 1200px;
  justify-content: space-between;
  align-items: center;
  background-color: #f1f1f1;
  padding: 1rem;
  border-radius: 8px;
}

.message-content {
  margin: 0;
}

.delete-btn {
  background-color: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.book-list {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.book {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}

.book img {
  width: 150px;
  height: 200px;
  object-fit: cover;
  margin-bottom: 10px;
}

.book-info h4 {
  margin: 0;
  font-size: 18px;
  margin-bottom: 5px;
}

.book-info p {
  margin: 0;
  font-size: 14px;
}

.filtered {
  margin-top: 40px;
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

.card-cover {
  width: 100px;
  height: 150px;
  object-fit: cover;
  margin-right: 20px;
}

.book-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.borrow-btn {
  background-color: #a8dadc;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 10px;
}

.borrow-btn:hover {
  background-color: #7ac1c9;
}

.borrow-btn:focus {
  outline: none;
}

.button-disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>