from flask import Blueprint, request, jsonify
import mysql.connector
from collections import defaultdict
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori
import datetime as dt

admin = Blueprint('admin', __name__)

db_config = {
    'user': 'root',
    'password': 'mysql123',
    'host': 'localhost',
    'database': 'library_system',
    'raise_on_warnings': True
}


def create_conn():
    return mysql.connector.connect(**db_config)


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


# 添加用户
@admin.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    is_admin = data.get('is_admin', False)

    conn = create_conn()
    cursor = conn.cursor()

    try:
        insert_query = """
            INSERT INTO users (username, email, password, is_admin)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query,
                       (data['username'], data['email'], data['password'], is_admin))
        conn.commit()

        user_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201

    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500


# 获取所有用户信息
@admin.route('/users', methods=['GET'])
def get_user():
    conn = create_conn()
    cursor = conn.cursor()

    try:
        query = """
            SELECT id,username,email,password,is_admin FROM users
        """
        cursor.execute(query)
        users = cursor.fetchall()
        result = []
        for i in users:
            l = list(i)
            user_profile = get_user_profile(i[0])
            if user_profile != None:
                query1 = """
                SELECT title FROM books
                WHERE category = %s or author = %s or FIND_IN_SET(%s,tags)
                """
                cursor.execute(query1, (user_profile, user_profile, user_profile,))
                books = cursor.fetchall()
                l.append(books)
                result.append(l)
            else:
                books = None
                l.append(books)
                result.append(l)
        return jsonify(result)

        if users is None:
            return jsonify({'error': 'User not found'}), 404

        cursor.close()
        conn.close()

        return jsonify(users), 200

    except mysql.connector.Error as err:
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500


# 修改用户信息
@admin.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    is_admin = data.get('is_admin', False)

    conn = create_conn()
    cursor = conn.cursor()

    try:
        update_query = """
            UPDATE users
            SET username = %s, email = %s, password = %s, is_admin = %s
            WHERE id = %s
        """
        cursor.execute(update_query,
                       (data['username'], data['email'], data['password'], is_admin,
                        user_id))

        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'User updated successfully'}), 200

    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500


# 删除用户
@admin.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = create_conn()
    cursor = conn.cursor()

    try:
        delete_query = """
            DELETE FROM users
            WHERE id = %s
        """
        cursor.execute(delete_query, (user_id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'User deleted successfully'}), 200

    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500


# 获取所有图书信息
@admin.route('/books', methods=['GET'])
def get_book():
    conn = create_conn()
    cursor = conn.cursor()

    try:
        query = """
            SELECT * FROM books
        """
        cursor.execute(query)
        books = cursor.fetchall()
        if books is None:
            return jsonify({'error': 'book not found'}), 404
        result = []
        for i in books:
            l = list(i)
            id = l[0]
            query1 = """
            SELECT comment from borrow_records
            where book_id = %s AND comment <> ''
            """
            cursor.execute(query1, (id,))
            comments = cursor.fetchall()
            if len(comments) == 0:
                comments = None
            l.append(comments)
            result.append(l)

        cursor.close()
        conn.close()
        return jsonify(result), 200


    except mysql.connector.Error as err:
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500


# 创建图书
@admin.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn', None)
    description = data.get('description', None)
    category = data.get('category', None)
    tags = data.get('tags', None)
    cover = data.get('cover', None)
    connection = create_conn()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, isbn, description, category, tags,cover) VALUES (%s, %s, %s, %s, %s, %s,%s)",
        (title, author, isbn, description, category, tags, cover))
    connection.commit()

    response = jsonify(message='Book created successfully')
    response.status_code = 201
    return response


# 更新图书
@admin.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()

    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn', None)
    description = data.get('description', None)
    category = data.get('category', None)
    tags = data.get('tags', None)
    cover = data.get('cover', None)

    connection = create_conn()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE books SET title = %s, author = %s, isbn = %s, description = %s, category = %s, tags = %s,cover=%s WHERE id = %s",
        (title, author, isbn, description, category, tags, cover, book_id))
    connection.commit()

    if cursor.rowcount:
        return jsonify(message='Book updated successfully')
    else:
        return jsonify(message='Book not found'), 404


# 删除图书
@admin.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    connection = create_conn()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    connection.commit()

    if cursor.rowcount:
        return jsonify(message='Book deleted successfully')
    else:
        return jsonify(message='Book not found'), 404


# 获取所有借阅信息
@admin.route('/borrows', methods=['GET'])
def get_borrow_records():
    conn = create_conn()
    cursor = conn.cursor()

    try:
        query = """
            SELECT * FROM borrow_records
        """
        cursor.execute(query)
        borrows = cursor.fetchall()

        if borrows is None:
            return jsonify({'error': 'record not found'}), 404
        data = []
        for borrow in borrows:
            l = list(borrow)
            l[3] = str(l[3])
            l[4] = str(l[4])
            l[5] = str(l[5])
            data.append(l)
        cursor.close()
        conn.close()

        return jsonify(data), 200

    except mysql.connector.Error as err:
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500


# 创建借阅记录
@admin.route('/borrow_records', methods=['POST'])
def create_borrow_record():
    data = request.get_json()

    user_id = data.get('user_id')
    book_id = data.get('book_id')
    borrow_date = data.get('borrow_date')
    return_date = data.get('return_date')
    due_date = data.get('due_date')

    connection = create_conn()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO borrow_records (user_id, book_id, borrow_date,return_date, due_date) VALUES (%s, %s, %s, %s,%s)",
        (user_id, book_id, borrow_date, return_date, due_date))
    connection.commit()

    response = jsonify(message='Borrow record created successfully')
    response.status_code = 201
    return response


# 更新借阅记录
@admin.route('/borrow_records/<int:record_id>', methods=['PUT'])
def update_borrow_record(record_id):
    data = request.get_json()
    return_date = data.get('return_date')

    connection = create_conn()
    cursor = connection.cursor()
    cursor.execute("UPDATE borrow_records SET return_date = %s WHERE id = %s", (return_date, record_id))
    connection.commit()

    if cursor.rowcount:
        return jsonify(message='Borrow record updated successfully')
    else:
        return jsonify(message='Borrow record not found'), 404


# 删除借阅记录
@admin.route('/borrow_records/<int:record_id>', methods=['DELETE'])
def delete_borrow_record(record_id):
    connection = create_conn()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM borrow_records WHERE id = %s", (record_id,))
    connection.commit()

    if cursor.rowcount:
        return jsonify(message='Borrow record deleted successfully')
    else:
        return jsonify(message='Borrow record not found'), 404


# 获取用户对系统的评论
@admin.route('/comments_sys', methods=['GET'])
def get_comm_sys():
    connection = create_conn()
    cursor = connection.cursor()
    query1 = """
              SELECT id AS user_id, comment
              FROM users
              WHERE comment <> ''
    """

    cursor.execute(query1)
    rows1 = cursor.fetchall()

    return jsonify(rows1)


# 获取用户对图书的评论

@admin.route('/comments_books', methods=['GET'])
def get_comm_books():
    connection = create_conn()
    cursor = connection.cursor()
    query1 = """
              SELECT user_id, book_id, comment
              FROM borrow_records
              WHERE comment <> ''
    """

    cursor.execute(query1)
    rows1 = cursor.fetchall()

    return jsonify(rows1)


@admin.route('/recommends', methods=['GET'])
def get_recommends():
    conn = create_conn()
    cursor = conn.cursor()
    # 执行查询
    query = "SELECT  id,username FROM users"
    cursor.execute(query)
    result = []
    data = cursor.fetchall()
    for i in data:
        l = list(i)
        profile = get_user_profile(l[0])
        l.append(profile)
        result.append(l)
    return jsonify(result)


# 评价反馈
@admin.route('/reply/<int:user_id>', methods=['PUT'])
def reply(user_id):
    data = request.get_json()

    conn = create_conn()
    cursor = conn.cursor()

    try:
        update_query = """
            UPDATE users
            SET reply = %s
            WHERE id = %s
        """
        cursor.execute(update_query,
                       (data['reply'], user_id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'User updated successfully'}), 200

    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500


# 活动发布
@admin.route('/activities', methods=["POST"])
def create_activity():
    data = request.get_json()

    if 'content' not in data or 'publish_time' not in data or 'deadline_time' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    conn = create_conn()
    cursor = conn.cursor()

    try:
        insert_query = """
            INSERT INTO activities (content,publish_time,deadline_time)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query,
                       (data['content'], data['publish_time'], data['deadline_time']))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'activity published successfully'}), 201

    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500


# 获取活动
@admin.route('/activities', methods=["GET"])
def get_activity():
    conn = create_conn()
    cursor = conn.cursor()

    try:
        query = """
            SELECT * FROM activities
        """
        cursor.execute(query)
        data = cursor.fetchall()
        activities = []
        for i in data:
            l = list(i)
            l[2] = str(l[2])
            l[3] = str(l[3])
            activities.append(l)
        cursor.close()
        conn.close()

        return jsonify(activities), 200

    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500
