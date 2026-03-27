import requests
import random

url = "http://127.0.0.1:5000/number"

# GET запрос
param = random.randint(1, 10)
get_res = requests.get(url, params={"param": param}).json()
print("GET запрос:", get_res)

# POST запрос
jsonparam = random.randint(1, 10)
post_res = requests.post(url, json={"jsonParam": jsonparam}).json()
print("POST запрос:", post_res)

# DELETE запрос
del_res = requests.delete(url).json()
print("DELETE запрос:", del_res)

def calc(x, y, operation):
    if operation == "sum":
        return x + y
    elif operation == "sub":
        return x - y
    elif operation == "mul":
        return x * y
    elif operation == "div":
        if y == 0:
            return "Деление на ноль невозможно"
        return x / y
    
# GET запрос
num_res = get_res['number']
print(f"Значение GET: {num_res}")

# POST запрос
num_res = calc(num_res, post_res['number'], post_res['operation'])
print(f"Значение POST ({post_res['operation']} {post_res['number']}): {num_res}")

# DELETE запрос
num_res = calc(num_res, del_res['number'], del_res['operation'])
print(f"Значение DELETE ({del_res['operation']} {del_res['number']}): {num_res}")

print("Итоговый результат:", num_res)
