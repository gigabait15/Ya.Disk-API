from flask import render_template, url_for, request, flash, redirect
from flask_login import login_user, login_required, logout_user
from src.config import login_manager, url, app, Users, items
from src.psql_db import User, add_db, get_users
from src.ya_api import get
from werkzeug.security import generate_password_hash, check_password_hash


login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/', methods=['POST', 'GET'])
@login_required
def submit_path():
    if request.method == 'POST':
        path = request.form.get('path')
        if path:
            return redirect(url_for('list_item', path=path))
        else:
            flash('Пожалуйста, введите путь.', 'error')
            return redirect(url_for('submit_path'))
    return render_template('submit_path.html')


@app.route('/list_item')
@login_required
async def list_item():
    path = request.args.get('path')
    if path:
        items = await get(url, path)
        return render_template('list_item.html', items=items)
    else:
        flash('Нет ссылки на публичный диск.', 'error')
        return redirect(url_for('submit_path'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_users(username, *items)

        if user and check_password_hash(user[3], password):
            login_user(User.get(user[0]))
            return redirect(url_for('submit_path'))
        else:
            flash('Неверный логин или пароль', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        if (len(request.form['username']) > 4 and
                len(request.form['email']) > 4 and
                len(request.form['password']) > 4 and
                request.form['password'] == request.form['confirm_password']):

            existing_user = get_users(request.form['username'], *items)
            if existing_user[1] == request.form['username'] and existing_user[2] == request.form['email']:
                return render_template('register.html', error='Пользователь уже существует.')

            hash = generate_password_hash(request.form['password'])
            user = Users(request.form['username'], request.form['email'], hash)
            reg = add_db(user)
            if reg:
                flash('Вы успешно зарегистрированы', 'success')
                return redirect(url_for('login'))
        else:
            flash('Неверно заполнены поля', 'error')
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
