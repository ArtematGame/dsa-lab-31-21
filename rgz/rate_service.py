from flask import Flask, request, jsonify

app = Flask(__name__)

# курс валют
@app.route("/rate")
def rate():
    try:
        currency = request.args.get("currency")

        rates = {
            "USD": 90.00,
            "EUR": 100.00
        }

        if currency not in rates:
            return jsonify({"message": "UNKNOWN CURRENCY"}), 400

        return jsonify({"rate": rates[currency]}), 200

    except Exception:
        return jsonify({"message": "UNEXPECTED ERROR"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)