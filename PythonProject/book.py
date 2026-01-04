from flask import Blueprint, render_template, request, redirect, url_for
from db import get_connection

book_bp = Blueprint('book', __name__)

# 图书列表（网页）
@book_bp.route('/list')
def list_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    conn.close()
    return render_template('book_list.html', books=books)

# 添加图书（表单提交）
@book_bp.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    category = request.form['category']
    total_count = int(request.form['total_count'])

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO book (title, author, isbn, category, total_count, available_count)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, author, isbn, category, total_count, total_count))
    conn.commit()
    conn.close()

    return redirect(url_for('book.list_books'))
