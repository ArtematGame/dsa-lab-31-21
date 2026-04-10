from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# База данных - словарь
users_db = {}
next_id = 1

# Класс User для совместимости с flask_login
class User(UserMixin):
    def __init__(self, id, email, name, password_hash):
        self.id = id
        self.email = email
        self.name = name
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    for email, user_data in users_db.items():
        if str(user_data['id']) == user_id:
            return User(user_data['id'], email, user_data['name'], user_data['password'])
    return None

# 1. Корневая страница GET /
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

# 2. Страница входа GET /login
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

# 3. Авторизация POST /login
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user_data = users_db.get(email)
    
    if not user_data:
        flash('Пользователь не найден')
        return render_template('login.html')
    
    if not check_password_hash(user_data['password'], password):
        flash('Неверный пароль')
        return render_template('login.html')
    
    user = User(user_data['id'], email, user_data['name'], user_data['password'])
    login_user(user)
    return redirect(url_for('index'))

# 4. Страница регистрации GET /signup
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

# 5. Регистрация POST /signup
@app.route('/signup', methods=['POST'])
def signup_post():
    global next_id
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email in users_db:
        flash('Пользователь уже существует')
        return render_template('signup.html')
    
    hashed_password = generate_password_hash(password)
    
    users_db[email] = {
        'id': next_id,
        'name': name,
        'password': hashed_password
    }
    next_id += 1
    
    return redirect(url_for('login'))

# 6. Выход GET /logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)