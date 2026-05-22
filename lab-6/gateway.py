from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests

app = Flask(__name__)

# Адреса микросервисов
currency_manager_url = "http://localhost:5001"
data_manager_url = "http://localhost:5002"

# HTML страницы
@app.route('/')
def index():
    # Получаем список валют для отображения
    try:
        resp = requests.get(f"{data_manager_url}/currencies")
        currencies_data = resp.json()
        currencies = currencies_data.get('currencies', [])
    except:
        currencies = []
    
    return render_template('index.html', currencies=currencies)

# Прокси для currency-manager
@app.route('/api/load', methods=['POST'])
def load():
    if request.is_json:
        data = request.get_json()
    else:
        data = {
            'currency_name': request.form.get('currency_name'),
            'rate': request.form.get('rate')
        }
    resp = requests.post(f"{currency_manager_url}/load", json=data)
    return redirect(url_for('index'))

@app.route('/api/update_currency', methods=['POST'])
def update():
    if request.is_json:
        data = request.get_json()
    else:
        data = {
            'currency_name': request.form.get('currency_name'),
            'rate': request.form.get('rate')
        }
    resp = requests.post(f"{currency_manager_url}/update_currency", json=data)
    return redirect(url_for('index'))

@app.route('/api/delete', methods=['POST'])
def delete():
    if request.is_json:
        data = request.get_json()
    else:
        data = {
            'currency_name': request.form.get('currency_name')
        }
    resp = requests.post(f"{currency_manager_url}/delete", json=data)
    return redirect(url_for('index'))

# Прокси для data-manager
@app.route('/api/currencies', methods=['GET'])
def currencies():
    resp = requests.get(f"{data_manager_url}/currencies")
    return jsonify(resp.json()), resp.status_code

@app.route('/api/convert', methods=['GET'])
def convert():
    name = request.args.get('currency_name')
    amount = request.args.get('amount')
    resp = requests.get(
        f"{data_manager_url}/convert",
        params={"currency_name": name, "amount": amount}
    )
    if resp.status_code == 200:
        result = resp.json().get('converted_amount_rub')
    else:
        result = "Ошибка конвертации"
    return redirect(f'/?result={result}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)