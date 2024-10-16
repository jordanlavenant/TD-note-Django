from flask import Flask, render_template, flash, request
import requests

app = Flask(__name__)

BASE_URL = 'http://localhost:8000/api/'

PRODUCT_STATUS = {
    0: 'Hors ligne',
    1: 'En ligne',
    2: 'En rupture de stock'
}

def get_products(search_query=None):
    try:
        params = {'search': search_query} if search_query else {}
        response = requests.get(f'{BASE_URL}products/', params=params)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_product(product_id):
    try:
        response = requests.get(f'{BASE_URL}products/{product_id}/')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    search_query = request.args.get('search')
    products = get_products(search_query)
    if products is None:
        flash('Failed to connect to the API. Please try again later.', 'error')
        products = []
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product(product_id)
    if product is None:
        flash('Failed to retrieve product details. Please try again later.', 'error')
        return render_template('product_detail.html', product={})
    return render_template('product_detail.html', product=product, get_status=get_status)

def get_status(status_code):
    return PRODUCT_STATUS.get(status_code, 'Unknown status')

if __name__ == '__main__':
    app.run(debug=True)