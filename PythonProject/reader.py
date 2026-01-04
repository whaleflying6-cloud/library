from flask import Blueprint, render_template, request, redirect, url_for
from db import get_connection

reader_bp = Blueprint('reader', __name__)


# 读者列表页面
@reader_bp.route('/list')
def list_readers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reader")
    readers = cursor.fetchall()
    conn.close()

    return render_template('reader_list.html', readers=readers)


# 添加读者（表单提交）
@reader_bp.route('/add', methods=['POST'])
def add_reader():
    name = request.form['name']
    student_no = request.form['student_no']
    reader_type = request.form['type']
    max_borrow = int(request.form.get('max_borrow', 5))  # 默认借阅上限5本

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reader (name, student_no, type, max_borrow)
        VALUES (%s, %s, %s, %s)
    """, (name, student_no, reader_type, max_borrow))
    conn.commit()
    conn.close()

    return redirect(url_for('reader.list_readers'))


# 删除读者
@reader_bp.route('/delete/<int:reader_id>')
def delete_reader(reader_id):
    conn = get_connection()
    cursor = conn.cursor()

    # 检查该读者是否有未还图书
    cursor.execute("""
        SELECT COUNT(*) FROM borrow_record 
        WHERE reader_id = %s AND status = 'borrowing'
    """, (reader_id,))
    borrowing_count = cursor.fetchone()[0]

    if borrowing_count > 0:
        conn.close()
        return f"该读者还有 {borrowing_count} 本图书未归还，不能删除。"

    cursor.execute("DELETE FROM reader WHERE id = %s", (reader_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('reader.list_readers'))