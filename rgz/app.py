from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import requests

app = Flask(__name__)

app.secret_key = "my_secret_key"

DB_CONFIG = {
    "host": "localhost",
    "database": "finance_db",
    "user": "postgres",
    "password": "postgres"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Таблица пользователей
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            login VARCHAR(100) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    """)

    # Таблица операций
    cur.execute("""
        CREATE TABLE IF NOT EXISTS operations (
            id SERIAL PRIMARY KEY,
            operation_date DATE NOT NULL,
            operation_sum NUMERIC(10, 2) NOT NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            type_operation VARCHAR(20) NOT NULL,
            payment_method VARCHAR(20)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    message = request.args.get("message", "")
    return render_template("index.html", message=message)

@app.route("/register")
def register_page():
    message = request.args.get("message", "")
    return render_template("register.html", message=message)

# Обработка регистрации
@app.route("/reg", methods=["POST"])
def reg():
    login = request.form.get("login")
    password = request.form.get("password")

    if not login or not password:
        return redirect("/register?message=Введите логин и пароль")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE login = %s", (login,))
        user = cur.fetchone()

        if user:
            cur.close()
            conn.close()
            return redirect("/register?message=Пользователь с таким логином уже существует")

        password_hash = generate_password_hash(password)

        cur.execute(
            "INSERT INTO users (login, password_hash) VALUES (%s, %s)",
            (login, password_hash)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/login?message=Регистрация прошла успешно. Теперь войдите")

    except Exception:
        return redirect("/register?message=Ошибка при регистрации")


@app.route("/login", methods=["GET", "POST"])
def login():
    message = request.args.get("message", "")

    if request.method == "POST":
        login_value = request.form.get("login")
        password = request.form.get("password")

        if not login_value or not password:
            return render_template("login.html", message="Введите логин и пароль")

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT id, password_hash FROM users WHERE login = %s",
                (login_value,)
            )

            user = cur.fetchone()

            cur.close()
            conn.close()

            if user and check_password_hash(user[1], password):
                session["user_id"] = user[0]
                session["login"] = login_value

                return redirect("/operations")

            return render_template("login.html", message="Неверный логин или пароль")

        except Exception:
            return render_template("login.html", message="Ошибка при входе")

    return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/?message=Вы вышли из аккаунта")

@app.route("/add_operation", methods=["GET", "POST"])
def add_operation():
    if "user_id" not in session:
        return redirect("/?message=Сначала нужно войти")

    message = ""

    if request.method == "POST":
        type_operation = request.form.get("type_operation")
        operation_sum = request.form.get("operation_sum")
        operation_date = request.form.get("operation_date")
        payment_method = request.form.get("payment_method")

        if not type_operation or not operation_sum or not operation_date:
            message = "Заполните тип операции, сумму и дату"
            return render_template("add_operation.html", message=message)

        if type_operation not in ["income", "expense"]:
            message = "Некорректный тип операции"
            return render_template("add_operation.html", message=message)

        # Если доход — способ оплаты не нужен
        if type_operation == "income":
            payment_method = None

        # Если расход — способ оплаты обязателен
        if type_operation == "expense":
            if payment_method not in ["НАЛИЧНЫЕ", "КАРТА"]:
                message = "Для расхода нужно выбрать способ оплаты"
                return render_template("add_operation.html", message=message)

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO operations
                (operation_date, operation_sum, user_id, type_operation, payment_method)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                operation_date,
                operation_sum,
                session["user_id"],
                type_operation,
                payment_method
            ))

            conn.commit()
            cur.close()
            conn.close()

            message = "Операция успешно добавлена"

        except Exception:
            message = "Ошибка при добавлении операции"

    return render_template("add_operation.html", message=message)

# просмотр операций
@app.route("/operations")
def operations():
    if "user_id" not in session:
        return redirect("/?message=Сначала нужно войти")

    try:
        currency = request.args.get("currency", "RUB")

        rate = 1

        # Если выбрали USD или EUR, получаем курс из внешнего сервиса
        if currency in ["USD", "EUR"]:
            response = requests.get(
                "http://127.0.0.1:5001/rate",
                params={"currency": currency}
            )

            if response.status_code == 200:
                rate = response.json()["rate"]
            else:
                return "Ошибка получения курса валют", 500

        elif currency == "RUB":
            rate = 1

        else:
            currency = "RUB"
            rate = 1

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, operation_date, operation_sum, type_operation, payment_method
            FROM operations
            WHERE user_id = %s
            ORDER BY operation_date DESC
        """, (session["user_id"],))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        operations_list = []

        for row in rows:
            operation_id = row[0]
            operation_date = row[1]
            operation_sum_rub = float(row[2])
            type_operation = row[3]
            payment_method = row[4]

            converted_sum = operation_sum_rub / rate

            operations_list.append({
                "id": operation_id,
                "date": operation_date,
                "sum": round(converted_sum, 2),
                "type_operation": type_operation,
                "payment_method": payment_method
            })

        return render_template(
            "operations.html",
            operations=operations_list,
            currency=currency
        )

    except Exception:
        return "Ошибка сервера", 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)