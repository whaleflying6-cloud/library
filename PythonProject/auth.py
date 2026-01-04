from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_connection

auth_bp = Blueprint('auth', __name__)

# 登录页面和处理登录
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 查询数据库中的用户
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()  # 获取单个用户
        conn.close()

        # 检查明文密码是否匹配
        if user and user['password'] == password:  # 不再使用加密验证
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('登录成功！', 'success')
            return redirect(url_for('index'))  # 登录成功后跳转到主页
        else:
            flash('用户名或密码错误', 'danger')

    return render_template('login.html')
