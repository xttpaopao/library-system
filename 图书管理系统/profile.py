from flask import Blueprint, request, jsonify
import mysql.connector
from datetime import datetime, timedelta

db_config = {
    'user': 'root',
    'password': 'mysql123',
    'host': 'localhost',
    'database': 'library_system',
    'raise_on_warnings': True
}


def create_conn():
    return mysql.connector.connect(**db_config)


profile = Blueprint('profile', __name__)


# 获取单个用户信息
@profile.route('/user/<int:user_id>', methods=['GET'])
def get_usr_profile(user_id):
    conn = create_conn()
    cursor = conn.cursor()
    query = "SELECT username,email,password FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    data = cursor.fetchone()
    return jsonify(data)


# 展示已经借阅的书籍
@profile.route('/profile/borrowed/<int:user_id>', methods=['GET'])
def get_usr_borrowed(user_id):
    conn = create_conn()
    cursor = conn.cursor()
    query = """
    SELECT id,book_id,borrow_date,due_date FROM borrow_records
    WHERE user_id = %s and isnull(return_date)
    ORDER BY return_date
    """
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    borrowed = []
    for i in data:
        l = list(i)
        book_id = l[1]
        l[2] = str(l[2])
        l[3] = str(l[3])
        query1 = """
        SELECT title,author,description,category,cover,num FROM books
        WHERE id = %s
        """
        cursor.execute(query1, (book_id,))
        result = cursor.fetchall()
        l.append(result)
        borrowed.append(l)

    return jsonify(borrowed)


# 展示已经预约的书籍
@profile.route("/profile/reserved/<int:user_id>", methods=["GET"])
def get_usr_reserved(user_id):
    conn = create_conn()
    cursor = conn.cursor()
    query = """
    SELECT * FROM user_reservations
    WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    reserved = []
    for i in data:
        l = list(i)
        book_id = l[2]
        query1 = """
                SELECT title,author,description,category,cover,num FROM books
                WHERE id = %s
                """
        cursor.execute(query1, (book_id,))
        result = cursor.fetchall()
        l.append(result)
        reserved.append(l)

    return jsonify(reserved)


# 续借
@profile.route('/profile/continueborrow/<int:borrow_id>', methods=["PUT"])
def extend_due_date(borrow_id):
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT due_date FROM borrow_records WHERE id = %s", (borrow_id,))
    original_due_date = cursor.fetchone()
    if original_due_date is None:
        return jsonify({"error": "Record not found"}), 404
    # 计算新的 due_date
    new_due_date = original_due_date[0] + timedelta(days=7)
    # 更新 due_date
    cursor.execute("UPDATE borrow_records SET due_date = %s WHERE id = %s", (new_due_date, borrow_id))
    conn.commit()

    return jsonify({"message": "Due date extended successfully", "new_due_date": new_due_date.isoformat()}), 200


# 还书
@profile.route('/profile/return/<int:borrow_id>', methods=['PUT'])
def return_book(borrow_id):
    conn = create_conn()
    cursor = conn.cursor()
    # 生成归还时间
    return_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("UPDATE borrow_records SET return_date = %s WHERE id = %s", (return_date, borrow_id))
    conn.commit()

    return jsonify({"message": "return successfully"}), 200


# 处理用户消息
@profile.route('/profile/messege/<int:user_id>', methods=["GET"])
def get_usr_messege(user_id):
    conn = create_conn()
    cursor = conn.cursor()
    # 提醒还书
    query_return = """
    SELECT book_id,borrow_date
    FROM borrow_records
    WHERE user_id = %s
    AND return_date IS NULL
    AND due_date = DATE(NOW()) + INTERVAL 1 DAY;
    """
    cursor.execute(query_return, (user_id,))
    borrow = cursor.fetchall()
    borrow_messege = []
    for i in borrow:
        l = list(i)
        book_id = l[0]
        cursor.execute("SELECT title from books WHERE id = %s", (book_id,))
        title = cursor.fetchall()
        l.append(list(title)[0][0])
        borrow_str = "还书提醒：" + "您于" + f"{l[1]}" + f"借阅的《{l[2]}》" + "距离归还已不到一天，请尽快归还"
        borrow_messege.append(borrow_str)
    # 预约成功
    query_reserve = """
    SELECT book_id FROM user_reservations
    WHERE user_id = %s
    """
    cursor.execute(query_reserve, (user_id,))
    reserve = cursor.fetchall()
    reserve_messege = []
    for i in reserve:
        l = list(i)
        book_id = l[0]
        cursor.execute("SELECT title from books WHERE id = %s", (book_id,))
        title = cursor.fetchall()
        l.append(list(title)[0][0])
        reserve_str = f"预约提醒：《{l[1]}》预约成功"
        reserve_messege.append(reserve_str)
    # 活动通知
    activity_messege = []
    cursor.execute("SELECT content,publish_time,deadline_time FROM activities")
    activity = cursor.fetchall()
    for i in activity:
        l = list(i)
        activity_str = f"活动提醒：{l[0]}，时间：{l[1]}~{l[2]}"
        activity_messege.append(activity_str)
    # 评论反馈
    reply_messege = []
    cursor.execute("SELECT comment,reply FROM users WHERE id = %s", (user_id,))
    reply = cursor.fetchall()
    for i in reply:
        l = list(i)
        reply_str = f"反馈提醒：您向系统提出的建议：”{l[0]}“，管理员已回复:”{l[1]}“"
        reply_messege.append(reply_str)
    messege = borrow_messege + reserve_messege + activity_messege + reply_messege
    return jsonify(messege)
