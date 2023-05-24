<template>
  <meta name="referrer" content="no-referrer"/>
  <div id="app">
    <div class="card-container" v-if="cardVisible" @click="closeCard">
      <div class="card" @click.stop>
        <img :src="selectedBook[7]" alt="book cover" class="card-cover">
        <div class="book-info">
          <h4>书名：{{ selectedBook[1] }}</h4>
          <p>&nbsp;</p>
          <p>作者：{{ selectedBook[2] }}</p>
          <p>ISBN：{{ selectedBook[3] }}</p>
          <p>分类：{{ selectedBook[5] }}</p>
          <p>标签：{{ selectedBook[6] }}</p>
          <p>描述：{{ selectedBook[4] }}</p>
          <p>&nbsp;</p>
          <p>剩余：{{ selectedBook[8] }}本</p>
          <p>&nbsp;</p>
          <div class="container">
            <div class="input-wrapper">
                <textarea
                    class="comment-input"
                    v-model="comment"
                    maxlength="50"
                    placeholder="请输入评价"
                    @input="updateWordCount"
                ></textarea>
              <span class="word-count">{{ wordCount }} / 50</span>
            </div>
          </div>
          <p>&nbsp;</p>
          <button class="borrow-btn" v-if="borrowBookVisable" @click="borrowBook"
                  :class="{ 'button-disabled': borrowed }"
                  :disabled="borrowed">{{ borrowed ? '已借阅' : '借阅' }}
          </button>
          <button class="borrow-btn" @click="reserveBook" v-if="reserveBookVisable">预约</button>
        </div>
      </div>
    </div>

    <div class="dashboard">
      <div class="search-bar">
        <input type="text" v-model="searchText" @keyup.enter="searchBooks" placeholder="搜索书籍"/>
      </div>
      <div class="category-search">
        <h3>分类检索</h3>
        <div class="multi-filter">
          <div class="filter-group">
            <div class="filter-label">作者：</div>
            <div class="filter-options">
              <button
                  class="filter-option"
                  :class="{ active: selectedAuthor === author }"
                  v-for="author in authors"
                  :key="author"
                  @click="selectAuthor(author)"
              >
                <h8>{{ author }}</h8>
              </button>
            </div>
          </div>

          <div class="filter-group">
            <div class="filter-label">分类：</div>
            <div class="filter-options">
              <button
                  class="filter-option"
                  :class="{ active: selectedCategory === category }"
                  v-for="category in categories"
                  :key="category"
                  @click="selectCategory(category)"
              >
                {{ category }}
              </button>
            </div>
          </div>

          <div class="filter-group">
            <div class="filter-label">标签：</div>
            <div class="filter-options">
              <button
                  class="filter-option"
                  :class="{ active: selectedTag === tag }"
                  v-for="tag in tags"
                  :key="tag"
                  @click="selectTag(tag)"
              >
                {{ tag }}
              </button>
            </div>
          </div>
        </div>

        <div class="filtered">
          <h3></h3>
          <div class="book-list">
            <div class="book" v-for="book in filterBooks" :key="book[0]" @click="showBookDetails(book)">
              <img :src="book[7]" alt="book cover"/>
              <div class="book-info">
                <h4>{{ book[1] }}</h4>
                <p>{{ book[2] }}</p>
                <p>剩余:{{ book[8] }}本</p>
              </div>
            </div>
          </div>
        </div>
        <div class="hot-recommendations">
          <h3>热门推荐</h3>
          <div class="book-list">
            <div class="book" v-for="book in hotBooks" :key="book[0]" @click="showBookDetails(book)">
              <img :src="book[7]" alt="book cover"/>
              <div class="book-info">
                <h4>{{ book[1] }}</h4>
                <p>{{ book[2] }}</p>
                <p>剩余:{{ book[8] }}本</p>
              </div>
            </div>
          </div>
        </div>

        <div class="you-may-like" v-if="recommendVisable">
          <h3>你可能喜欢</h3>
          <div class="book-list">
            <div class="book" v-for="book in likedBooks" :key="book[0]" @click="showBookDetails(book)">
              <img :src="book[7]" alt="book cover"/>
              <div class="book-info">
                <h4>{{ book[1] }}</h4>
                <p>{{ book[2] }}</p>
                <p>剩余:{{ book[8] }}本</p>
              </div>
            </div>
          </div>
        </div>
        <div class="user-comment">
          <h3>请输入您对本系统的看法和建议，帮助我们更好改进</h3>
          <textarea
              class="comment-input"
              v-model="userComment"
              maxlength="100"
              @keyup.enter="commentCommit"
              placeholder="请输入评价"
          ></textarea>
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
      userComment: '',
      comment: '',
      wordCount: 0,
      borrowed: false,
      cardVisible: false,
      recommendVisable: false,
      reserveBookVisable: false,
      borrowBookVisable: true,
      selectedBook: null,
      searchText: "",
      filterBooks: [],
      hotBooks: [],
      likedBooks: [],
      authors: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],

      categories: [],
      tags: [],
      selectedAuthor: "",
      selectedCategory: "",
      selectedTag: "",
      categoryBooks: [],
    };
  },
  methods: {
    async reserveBook() {
      const userId = store.state.userId;
      try {
        const response = await axios.post(`http://localhost:5000/reserve/${userId}`, {
          user_id: userId,
          book_id: this.selectedBook[0]
        });

        if (response.data.message === 'reserve successfully') {
          setTimeout(() => {
            this.$message({
              message: "预约成功",
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
    async commentCommit() {
      try {
        const response = await axios.put(`http://localhost:5000/comment/${userId}`, {
          user_id: userId,
          comment: this.userComment
        });

        if (response.data.message === 'Comment updated successfully') {
          setTimeout(() => {
            this.$message({
              message: "评论成功",
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
    updateWordCount() {
      this.wordCount = this.comment.length;
    },
    async borrowBook() {
      // 获取用户ID和书籍ID
      const userId = store.state.userId;
      const bookId = this.selectedBook[0];
      const comment = this.comment;

      // 创建请求的数据对象
      const requestData = {
        userId: userId,
        bookId: bookId,
        comment: comment
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
    showBookDetails(book) {
      this.selectedBook = book;
      this.cardVisible = true;
      if (book[8] === 0) {
        this.borrowBookVisable = false;
        this.reserveBookVisable = true;
      } else {
        this.borrowed = false;
        this.borrowBookVisable = true;
        this.reserveBookVisable = false;
      }
    },
    closeCard() {
      this.cardVisible = false;
    },
    searchBooks() {
      // 将 searchText 传递给后端
      axios
          .post("http://localhost:5000/api/searchBooks", {searchText: this.searchText})
          .then((response) => {
            // 更新 filterBooks 为后端返回的搜索结果
            this.filterBooks = response.data;
          })
          .catch((error) => {
            console.error("Error fetching search results:", error);
          });
    },
    selectAuthor(author) {
      if (this.selectedAuthor === author) {
        // 如果已选定该作者，则取消选择
        this.selectedAuthor = null;
        this.applyFilters();
        this.fetchFilteredBooks();
      } else {
        // 如果未选定该作者，则进行选择
        this.selectedAuthor = author;
        this.applyFilters();
        this.fetchFilteredBooks();
      }
    },
    selectCategory(category) {
      if (this.selectedCategory === category) {
        // 如果已选定该作者，则取消选择
        this.selectedCategory = null;
        this.applyFilters();
        this.fetchFilteredBooks();
      } else {
        // 如果未选定该作者，则进行选择
        this.selectedCategory = category;
        this.applyFilters();
        this.fetchFilteredBooks();
      }
    },
    selectTag(tag) {
      if (this.selectedTag === tag) {
        // 如果已选定该作者，则取消选择
        this.selectedTag = null;
        this.applyFilters();
        this.fetchFilteredBooks();
      } else {
        // 如果未选定该作者，则进行选择
        this.selectedTag = tag;
        this.applyFilters();
        this.fetchFilteredBooks();
      }
    },
    applyFilters() {
      this.$emit("filter", {
        author: this.selectedAuthor,
        category: this.selectedCategory,
        tag: this.selectedTag,
      });
    },
    fetchFilteredBooks() {
      // 构建一个包含筛选条件的对象
      const filterParams = {
        author: this.selectedAuthor,
        category: this.selectedCategory,
        tag: this.selectedTag,
      };
      axios.post('http://localhost:5000/api/filterBooks', filterParams)
          .then((response) => {
            // 更新 filterBooks 为后端返回的数据
            this.filterBooks = response.data;
          })
          .catch((error) => {
            console.error('Error fetching filtered books:', error);
          });
    },
  },
  created() {
    const userId = store.state.userId;
    // axios.get('http://localhost:5000/api/authors').then((response) => {
    //   this.authors = response.data;
    // });

    axios.get('http://localhost:5000/api/categories').then((response) => {
      this.categories = response.data;
    });

    axios.get('http://localhost:5000/api/tags').then((response) => {
      this.tags = response.data;
    });
    axios.get('http://localhost:5000/api/random_15').then((response) => {
      this.filterBooks = response.data;
    });
    axios.get('http://localhost:5000/api/hotBooks').then((response) => {
      this.hotBooks = response.data;
    });
    axios.get(`http://localhost:5000/api/likedBooks/${userId}`).then((response) => {
      this.likedBooks = response.data;
      if (response.status === 200) {
        this.recommendVisable = true;
      }
      else {
        this.recommendVisable = false;
      }
    });
  },
};
</script>

<style scoped>
.multi-filter {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  gap: 15px; /* 添加间隙 */
}

.filter-group {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.filter-label {
  margin-right: 5px;
}

.filter-options {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.filter-option {
  margin-right: 10px;
  margin-bottom: 10px;;
  padding: 5px 10px;
  border: none;
  background-color: #f0f0f0;
  border-radius: 5px;
  cursor: pointer;
}

.filter-option.active {
  background-color: #5c6bc0;
  color: #fff;
}

.dashboard {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.search-bar {
  margin: 20px 0;
  display: flex;
  align-items: center;
}

.search-bar input[type="text"] {
  flex-grow: 1;
  padding: 10px 20px;
  font-size: 18px;
  border: 1px solid #ccc;
  border-radius: 25px; /* 圆角处理 */
  outline: none;
}

.search-bar button {
  margin-left: 10px;
  padding: 10px 20px;
  font-size: 18px;
  background-color: #5c6bc0;
  color: #fff;
  border: none;
  border-radius: 25px; /* 圆角处理 */
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

.filtered,
.hot-recommendations,
.you-may-like {
  margin-top: 40px;
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

.container {
  position: relative;
}

.input-wrapper {
  position: relative;
  display: inline-block;
}

.comment-input {
  width: 100%;
  height: 90px;
  resize: none;
  box-sizing: border-box;
}

.word-count {
  position: absolute;
  right: 5px;
  bottom: 5px;
  font-size: 12px;
  color: #999;
}

.category-search {
  max-width: 60%;
  margin: 0 auto; /* 这行代码会使容器在页面上居中 */
}
</style>