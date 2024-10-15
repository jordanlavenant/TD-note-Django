from flask import Flask, render_template
import requests

app = Flask(__name__)

BASE_URL = 'http://localhost:8000/api/'

def get_products():
    response = requests.get(f'{BASE_URL}products/')
    return response.json()

@app.route('/')
def index():
    products = get_products()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)