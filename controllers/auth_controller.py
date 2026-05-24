from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import Config
from database.connection import DatabaseConnection
from pymongo.errors import OperationFailure

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Введите имя пользователя и пароль', 'warning')
            return render_template('login.html')

        user_type = None
        for key, user_info in Config.USERS.items():
            if user_info['username'] == username and user_info['password'] == password:
                user_type = key
                break

        if user_type:
            user_info = Config.USERS[user_type]
            try:
                conn = DatabaseConnection.get_connection(username, password)
                db = conn.db
                db.command('ping')

                session['user'] = user_type
                session['db_username'] = username
                session['db_password'] = password
                session['role'] = user_info['role']
                session['permissions'] = user_info['permissions']

                flash(f'Успешный вход как {user_info["role"]} ({user_type})', 'success')
                return redirect(url_for('index'))

            except OperationFailure as e:
                flash(f'Ошибка БД: неверные учетные данные - {str(e)}', 'danger')
            except Exception as e:
                flash(f'Ошибка подключения: {str(e)}', 'danger')
        else:
            flash('Ошибка: неверное имя пользователя или пароль', 'danger')

    return render_template('login.html')

@auth_controller.route('/logout')
def logout():
    session.clear()
    DatabaseConnection.close_all()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth_controller.login'))