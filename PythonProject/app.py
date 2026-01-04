from flask import Flask, render_template, redirect, url_for, session
from db import get_connection
from book import book_bp
from borrow import borrow_bp
from reader import reader_bp
from auth import auth_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于加密 session

# 数据库连接测试
@app.route('/db_test')
def db_test():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    conn.close()
    return "数据库连接成功"

# 注册蓝图
app.register_blueprint(book_bp, url_prefix='/book')
app.register_blueprint(borrow_bp, url_prefix='/borrow')
app.register_blueprint(reader_bp, url_prefix='/reader')
app.register_blueprint(auth_bp, url_prefix='/auth')

# 主页，检查用户是否已登录
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('auth.login'))  # 如果没有登录，跳转到登录页面
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
