from flask import Blueprint, request, jsonify
import mysql.connector
from datetime import datetime, timedelta
from collections import defaultdict
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori
import datetime as dt
from pypinyin import lazy_pinyin

db_config = {
    'user': 'root',
    'password': 'mysql123',
    'host': 'localhost',
    'database': 'library_system',
    'raise_on_warnings': True
}


def create_conn():
    return mysql.connector.connect(**db_config)


users = Blueprint('users', __name__)


def get_initial(s):
    # 获取字符串的首字母并转为大写
    return lazy_pinyin(s)[0][0].upper()


def get_user_profile(user_id):
    # 数据库连接配置
    config = {
        'user': 'root',
        'password': 'mysql123',
        'host': 'localhost',
        'database': 'library_system'
    }

    # 连接到数据库
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # 执行 SQL 查询
    query = """
    SELECT users.id AS user_id, users.username, books.id AS book_id, books.category, books.tags, books.author, borrow_records.borrow_date
    FROM users
    JOIN borrow_records ON users.id = borrow_records.user_id
    JOIN books ON borrow_records.book_id = books.id
    """

    cursor.execute(query)

    # 将查询结果存储到 pandas DataFrame 中
    columns = ['user_id', 'username', 'book_id', 'category', 'tags', 'author', 'borrow_date']
    data = pd.DataFrame(cursor.fetchall(), columns=columns)
    data0 = data
    # 关闭数据库连接
    cursor.close()
    cnx.close()

    label_encoder = LabelEncoder()
    # 逐个特征进行编码
    data['user_encoded'] = label_encoder.fit_transform(data['username'])
    data['author_encoded'] = label_encoder.fit_transform(data['author'])
    data['category_encoded'] = label_encoder.fit_transform(data['category'])
    data['tag_encoded'] = label_encoder.fit_transform(data['tags'])
    data['borrow_date_timestamp'] = data['borrow_date'].apply(
        lambda x: dt.datetime.combine(x, dt.time.min).timestamp())

    # 删除原始的字符串特征列
    data = data.drop(columns=['username', 'category', 'tags', 'author', 'borrow_date'])

    # 聚类分析（以 K-means 为例）
    k = 10  # 您可以根据需要更改聚类数量
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(data)

    # 将聚类结果添加到原始数据中
    data['cluster'] = kmeans.labels_
    if data[data['user_id'] == user_id].size == 0:
        return None
    else:
        user_cluster = data.loc[data['user_id'] == user_id, 'cluster'].values[0]
    users = data0[data['cluster'] == user_cluster]

    # 将数据处理为适用于Apriori算法的形式
    transactions = defaultdict(set)
    for _, row in users.iterrows():
        user_id = row['user_id']
        category = row['category']
        tags = row['tags']
        author = row['author']

        transactions[user_id].add(category)
        transactions[user_id].add(tags)
        transactions[user_id].add(author)

    transactions = list(transactions.values())

    # 使用 TransactionEncoder 对事务数据进行转换
    encoder = TransactionEncoder()
    transactions_encoded = encoder.fit(transactions).transform(transactions)
    transactions_df = pd.DataFrame(transactions_encoded, columns=encoder.columns_)

    # 使用 mlxtend 库的 apriori 函数进行关联规则分析
    min_support = 0.1
    frequent_itemsets = apriori(transactions_df, min_support, use_colnames=True)
    max_support_itemset = list(frequent_itemsets.loc[frequent_itemsets['support'].idxmax(), 'itemsets'])
    return max_support_itemset[0]


# 用户登录
@users.route('/login', methods=['POST'])
def login():
    # 获取前端传来的数据
    username = request.json['username']
    password = request.json['password']
    # 连接数据库
    conn = create_conn()
    cursor = conn.cursor()

    # 查询该用户是否存在
    query = 'SELECT * FROM users WHERE username = %s'
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user is None:
        # 如果用户不存在，返回错误信息
        return jsonify({'message': 'User not found'}), 404
    elif password != user[3]:
        # 如果密码不匹配，返回错误信息
        return jsonify({'message': 'Incorrect password'}), 401
    else:
        # 判断用户是否为管理员
        is_admin = False
        if user[5] == 1:
            is_admin = True
        if is_admin == True:
            # 如果用户名和密码都匹配，返回成功信息
            return jsonify({'message': 'Admin Login successful', 'userId': user[0]}), 200
        else:
            return jsonify({'message': 'User Login successful', 'userId': user[0]}), 200

    cursor.close()
    conn.close()


# 用户注册
@users.route('/register', methods=['POST'])
def register():
    # 获取前端发送过来的数据
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    # 检查用户名是否已经存在
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    if result is not None:
        return jsonify({'message': '用户名已经存在'}), 400

    # 将用户信息插入到数据库中
    cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': '注册成功'}), 201


# 用户界面dashboard中的api
@users.route('/api/authors', methods=['GET'])
def get_authors():
    # 连接数据库
    conn = create_conn()
    cursor = conn.cursor()
    # 执行查询
    query = "SELECT DISTINCT author FROM books"
    cursor.execute(query)
    authors = [row[0] for row in cursor.fetchall()]
    return jsonify(authors)


@users.route('/api/categories', methods=['GET'])
def get_categories():
    # 连接数据库
    conn = create_conn()
    cursor = conn.cursor()
    # 执行查询
    query = "SELECT DISTINCT category FROM books"
    cursor.execute(query)
    categories = [row[0] for row in cursor.fetchall()]
    return jsonify(categories)


@users.route('/api/tags', methods=['GET'])
def get_tags():
    # 连接数据库
    conn = create_conn()
    cursor = conn.cursor()
    # 执行查询
    query = "SELECT DISTINCT tags FROM books"
    cursor.execute(query)
    tags = [row[0] for row in cursor.fetchall()]
    unique_tags = set()
    for tag in tags:
        unique_tags.update(tag.split(','))
    unique_tags = list(unique_tags)
    return jsonify(unique_tags)


@users.route('/api/filterBooks', methods=['POST'])
def get_filterBooks():
    # 前端发送的数据
    author = request.json['author']
    category = request.json['category']
    tag = request.json['tag']
    # 连接数据库
    conn = create_conn()
    cursor = conn.cursor()
    # 获取所有书籍信息
    query1 = "SELECT * FROM books"
    cursor.execute(query1)
    result = cursor.fetchall()

    # 关闭连接
    cursor.close()
    conn.close()

    # 将结果转为字典列表，并将作者名转换为拼音首字母
    books = [{'id': row[0], 'title': row[1], 'author': row[2], 'isbn': row[3], 'description': row[4],
              'category': row[5], "tags": row[6], 'cover': row[7], 'num': row[8], 'author_initial': get_initial(row[2])}
             for row
             in result]

    # 根据前端传递的参数进行筛选
    if author:
        books = [book for book in books if book['author_initial'] == author]
    if category:
        books = [book for book in books if book['category'] == category]
    if tag:
        books = [book for book in books if tag in book['tags'].split(',')]

    # 获取每个书籍信息的值，并转化为列表
    books_values = [list(book.values()) for book in books]
    return jsonify(books_values)


@users.route('/api/hotBooks', methods=['GET'])
def get_hotBooks():
    # 连接数据库
    conn = create_conn()
    cursor = conn.cursor()
    query = """
            SELECT *
                FROM books
                    WHERE books.id IN (
                      SELECT book_id
                      FROM (
                        SELECT book_id, COUNT(*) as cnt
                        FROM borrow_records
                        GROUP BY book_id
                        ORDER BY cnt DESC
                        LIMIT 8
                      ) as temp
            );
        """
    cursor.execute(query)
    hotBooks = cursor.fetchall()
    return jsonify(hotBooks)


@users.route('/api/random_15', methods=['GET'])
def get_random():
    # 连接数据库
    conn = create_conn()
    cursor = conn.cursor()
    query = """
            SELECT * FROM books
            ORDER BY RAND()
            LIMIT 15;
        """
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)


@users.route('/api/searchBooks', methods=['POST'])
def search_books():
    # 连接数据库
    conn = create_conn()
    cursor = conn.cursor()
    search_text = request.json['searchText']
    query = """
            SELECT * FROM books
            WHERE title LIKE %s OR author LIKE %s or category LIKE %s
            """
    cursor.execute(query, ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%',))
    result = cursor.fetchall()
    return jsonify(result)


# 接受借阅信息，保存到数据库
@users.route('/api/borrow', methods=['POST'])
def borrow_book():
    # 获取请求数据
    user_id = request.json.get('userId')
    book_id = request.json.get('bookId')
    comment = request.json.get('comment', None)

    # 获取当前日期并计算归还日期
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    conn = create_conn()
    cursor = conn.cursor()

    # 插入数据到borrow_records表
    query = """
        INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date,comment) VALUES (%s, %s, %s, %s,%s)
    """
    query2 = """
        UPDATE books SET num = num - 1 WHERE id = %s;
    """
    values = (user_id, book_id, borrow_date, due_date, comment)
    cursor.execute(query, values)
    cursor.execute(query2, (book_id,))
    cursor.execute("DELETE FROM user_reservations WHERE user_id = %s AND book_id = %s", (user_id, book_id,))
    conn.commit()
    # 关闭数据库连接
    cursor.close()
    conn.close()

    return jsonify({"message": "Borrow record added successfully!"})


# 个性化推荐
@users.route('/api/likedBooks/<int:user_id>', methods=['GET'])
def get_likedBooks(user_id):
    key = get_user_profile(user_id)
    if key != None:
        query1 = """
        SELECT * FROM books
        WHERE category = %s or author = %s or FIND_IN_SET(%s,tags)
        """
        conn = create_conn()
        cursor = conn.cursor()
        cursor.execute(query1, (key, key, key,))
        result1 = cursor.fetchall()
        return jsonify(result1), 200
    else:
        return jsonify({'message': 'fault'}), 500


# 用户对系统的评价，上传到users
@users.route('/comment/<int:user_id>', methods=['PUT'])
def update_comment(user_id):
    data = request.get_json()

    if 'user_id' not in data or 'comment' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    conn = create_conn()
    cursor = conn.cursor()

    try:
        update_query = """
            UPDATE users
            SET comment = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (data['comment'], data['user_id']))

        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Comment updated successfully'}), 200

    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500


@users.route('/reserve/<int:user_id>', methods=["POST"])
def reserve(user_id):
    data = request.get_json()
    if 'user_id' not in data or 'book_id' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    conn = create_conn()
    cursor = conn.cursor()

    try:
        update_query = "INSERT INTO user_reservations (user_id, book_id) VALUES (%s, %s)"
        cursor.execute(update_query, (user_id, data['book_id']))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'reserve successfully'}), 200

    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500
