from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host='localhost',
        port='5432',
        database='postgres',
        user='postgres',
        password='postgres'
    )

@app.route('/convert', methods=['GET'])
def convert_currency():
    currency_name = request.args.get('currency_name')
    amount_str = request.args.get('amount')

    if not currency_name:
        return jsonify({"error": "Не указан параметр currency_name"}), 400
    if not amount_str:
        return jsonify({"error": "Не указан параметр amount"}), 400

    try:
        amount = float(amount_str)
    except ValueError:
        return jsonify({"error": "Параметр amount должен быть числом"}), 400

    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cursor.execute(
            "SELECT currency_name, rate FROM currencies WHERE currency_name = %s",
            (currency_name,)
        )
        currency = cursor.fetchone()

        if not currency:
            cursor.close()
            conn.close()
            return jsonify({"error": f"Валюта '{currency_name}' не найдена в базе"}), 404

        rate = float(currency['rate'])
        converted_amount = amount * rate

        return jsonify({
            "currency": currency_name,
            "amount_in_currency": amount,
            "rate_to_rub": rate,
            "converted_amount_rub": round(converted_amount, 2)
        }), 200

    except Exception as e:
        return jsonify({"error": f"Ошибка сервера: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/currencies', methods=['GET'])
def get_all_currencies():
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cursor.execute("SELECT id, currency_name, rate FROM currencies ORDER BY id")
        currencies = cursor.fetchall()

        result = []
        for curr in currencies:
            result.append({
                "id": curr['id'],
                "currency_name": curr['currency_name'],
                "rate": float(curr['rate'])
            })

        return jsonify({
            "count": len(result),
            "currencies": result
        }), 200

    except Exception as e:
        return jsonify({"error": f"Ошибка сервера: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)