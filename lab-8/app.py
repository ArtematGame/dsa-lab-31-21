from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"], 
    storage_uri="memory://"
)

data_file = "data.json"

# Загрузка данных из файла 
def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Сохранение данных в файл п
def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# POST сохранить ключ-значение
@app.route("/set", methods=["POST"])
@limiter.limit("10 per minute")
def set_key():
    content = request.get_json()
    key = content.get("key")
    value = content.get("value")
    
    if not key or value is None:
        return jsonify({"error": "key и value обязательны"}), 400
    
    data[key] = value
    save_data(data)
    return jsonify({"status": "ok", "key": key, "value": value})

# GET получить значение по ключу
@app.route("/get/<key>", methods=["GET"])
def get_key(key):
    if key in data:
        return jsonify({"key": key, "value": data[key]})
    return jsonify({"error": "ключ не найден"}), 404

# DELETE удалить ключ
@app.route("/delete/<key>", methods=["DELETE"])
@limiter.limit("10 per minute")  # 10 запросов в минуту
def delete_key(key):
    if key in data:
        del data[key]
        save_data(data)
        return jsonify({"status": "deleted", "key": key})
    return jsonify({"error": "ключ не найден"}), 404

# GET проверить наличие ключа
@app.route("/exists/<key>", methods=["GET"])
def exists_key(key):
    return jsonify({"key": key, "exists": key in data})

if __name__ == "__main__":
    app.run(debug=True)