from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

def get_db():
    return psycopg2.connect (
        host = 'localhost',
        port = '5432',
        database = 'postgres',
        user = 'postgres',
        password = 'postgres'
    )

#эндпоинт 1

@app.route('/load', methods = ["POST"])
def load_currency ():
    data = request.get_json()
    currency_name = data.get('currency_name')
    rate = data.get('rate')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM currencies WHERE currency_name = %s", (currency_name,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Валюта уже существует"}), 400

    cursor.execute("INSERT INTO currencies (currency_name, rate) VALUES (%s, %s)",
        (currency_name, rate)                  
    )

    conn.commit()

    cursor.close()
    conn.close()
    
    return jsonify({"message": "Валюта добавлена"})

#эндпоинт 2

@app.route('/update_currency', methods=['POST'])
def update_currency():
    data = request.get_json()
    currency_name = data.get('currency_name')
    new_rate = data.get('rate')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверка: такая валюта существует в БД
    cursor.execute("SELECT id FROM currencies WHERE currency_name = %s", (currency_name,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Валюта не найдена"}), 404
    
    # Обновление курса
    cursor.execute("UPDATE currencies SET rate = %s WHERE currency_name = %s", (new_rate, currency_name))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Курс обновлен"}), 200

#эндпоинт 3

@app.route('/delete', methods=['POST'])
def delete_currency():
    data = request.get_json()
    currency_name = data.get('currency_name')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверка: такая валюта существует в БД
    cursor.execute("SELECT id FROM currencies WHERE currency_name = %s", (currency_name,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Валюта не найдена"}), 404
    
    # Удаление валюты
    cursor.execute("DELETE FROM currencies WHERE currency_name = %s", (currency_name,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Валюта удалена"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)