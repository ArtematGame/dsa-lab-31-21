from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 1 Раздел
# GET эндпоинт
@app.route('/number/', methods=['GET'])
def get_number():
    param = request.args.get('param')
    if param is None:
        return jsonify({"error": "param is required"}), 400
    
    param = int(param)
    random_num = random.randint(1, 100)
    result = random_num * param
    
    return jsonify({
        "random_number": random_num,
        "number": result,
    })

# POST эндпоинт
@app.route('/number/', methods=['POST'])
def post_number():
    data = request.get_json()
    jsonParam = data.get('jsonParam')
    
    if jsonParam is None:
        return jsonify({"error": "jsonParam is required"}), 400
    
    random_num = random.randint(1, 100)
    result = random_num * jsonParam
    
    return jsonify({
        "random_number": random_num,
        "number": result,
        "operation": random.choice(["sum", "sub", "mul", "div"])
    })

# DELETE эндпоинт
@app.route('/number/', methods=['DELETE'])
def delete_number():
    random_num = random.randint(1, 100)
    
    return jsonify({
        "random_number": random_num,
        "number": random_num,
        "operation": random.choice(["sum", "sub", "mul", "div"])
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)


