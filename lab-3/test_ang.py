import requests
import random

url = "http://127.0.0.1:5000/number/"

try:
    # 1. GET запрос
    print("\n1) GET запрос")
    param = random.randint(1, 10)
    print(f"param = {param}")
    
    r = requests.get(url, params={"param": param}).json()
    print(f"random_number={r['random_number']}, number={r['number']}, operation={r['operation']}")
    result = r["number"]
    expression = str(result)
    
    # 2. POST запрос
    print("\n2) POST запрос")
    jsonParam = random.randint(1, 10)
    print(f"jsonParam = {jsonParam}")
    
    r = requests.post(url, json={"jsonParam": jsonParam}).json()
    print(f"random_number={r['random_number']}, number={r['number']}, operation={r['operation']}")
    
    # Применяем операцию
    if r["operation"] == "sum":
        result += r["number"]
        expression += f" + {r['number']}"
    elif r["operation"] == "sub":
        result -= r["number"]
        expression += f" - {r['number']}"
    elif r["operation"] == "mul":
        result *= r["number"]
        expression += f" * {r['number']}"
    elif r["operation"] == "div":
        result /= r["number"]
        expression += f" / {r['number']}"
    
    print(f"{expression} = {result}")
    
    # 3. DELETE запрос
    print("\n3) DELETE запрос")
    r = requests.delete(url).json()
    print(f"random_number={r['random_number']}, number={r['number']}, operation={r['operation']}")
    
    # Применяем операцию
    if r["operation"] == "sum":
        result += r["number"]
        expression += f" + {r['number']}"
    elif r["operation"] == "sub":
        result -= r["number"]
        expression += f" - {r['number']}"
    elif r["operation"] == "mul":
        result *= r["number"]
        expression += f" * {r['number']}"
    elif r["operation"] == "div":
        result /= r["number"]
        expression += f" / {r['number']}"
    
    print(f"{expression} = {result}")
    print(f"\nРезультат: {int(result)}")

except Exception as error:
    print(f"\nОшибка: {error}")