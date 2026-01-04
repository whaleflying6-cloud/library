from flask import Blueprint, request, redirect, url_for, render_template
from db import get_connection
from datetime import date, timedelta

borrow_bp = Blueprint('borrow', __name__)


# 借书页面（显示可借图书和读者列表）
@borrow_bp.route('/')
def borrow_page():
    conn = get_connection()
    cursor = conn.cursor()

    # 获取所有可借图书（available_count > 0）
    cursor.execute("SELECT * FROM book WHERE available_count > 0")
    books = cursor.fetchall()

    # 获取所有读者
    cursor.execute("SELECT * FROM reader")
    readers = cursor.fetchall()

    # 获取借阅记录（用于显示）
    cursor.execute("""
        SELECT br.*, b.title, r.name 
        FROM borrow_record br
        JOIN book b ON br.book_id = b.id
        JOIN reader r ON br.reader_id = r.id
        WHERE br.status = 'borrowing'
    """)
    borrowing_records = cursor.fetchall()

    conn.close()

    return render_template('borrow.html',
                           books=books,
                           readers=readers,
                           records=borrowing_records)


# 执行借书操作
@borrow_bp.route('/borrow', methods=['POST'])
def borrow_book():
    reader_id = request.form['reader_id']
    book_id = request.form['book_id']

    conn = get_connection()
    cursor = conn.cursor()

    # 检查库存
    cursor.execute("SELECT available_count FROM book WHERE id = %s", (book_id,))
    available = cursor.fetchone()[0]

    if available <= 0:
        conn.close()
        return "库存不足"

    # 计算借阅日期和归还日期（默认30天）
    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=30)

    # 插入借阅记录
    cursor.execute("""
        INSERT INTO borrow_record 
        (reader_id, book_id, borrow_date, due_date, status)
        VALUES (%s, %s, %s, %s, 'borrowing')
    """, (reader_id, book_id, borrow_date, due_date))

    # 更新图书库存
    cursor.execute("""
        UPDATE book 
        SET available_count = available_count - 1 
        WHERE id = %s
    """, (book_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('borrow.borrow_page'))


# 还书操作
@borrow_bp.route('/return/<int:record_id>')
def return_book(record_id):
    conn = get_connection()
    cursor = conn.cursor()

    # 获取借阅记录对应的图书ID
    cursor.execute("SELECT book_id FROM borrow_record WHERE id = %s", (record_id,))
    book_id = cursor.fetchone()[0]

    # 更新借阅记录状态
    cursor.execute("""
        UPDATE borrow_record 
        SET status = 'returned', return_date = %s 
        WHERE id = %s
    """, (date.today(), record_id))

    # 恢复图书库存
    cursor.execute("""
        UPDATE book 
        SET available_count = available_count + 1 
        WHERE id = %s
    """, (book_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('borrow.borrow_page'))