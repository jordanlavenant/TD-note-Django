from flask import Flask, redirect, render_template, flash, request, session, url_for
import requests

app = Flask(__name__)
app.secret_key = 'secret_key'

BASE_URL = 'http://localhost:8000/api/'

def get_status(status_code):
    PRODUCT_STATUS = {
        0: 'Hors ligne',
        1: 'En ligne',
        2: 'En rupture de stock'
    }
    return PRODUCT_STATUS.get(status_code, 'Unknown status')

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

@app.before_request
def initialize_balance():
    if 'balance' not in session:
        session['balance'] = 100.0
    
@app.context_processor
def inject_balance():
    return {'balance': session.get('balance', 0.0)}

@app.route('/add_balance', methods=['POST'])
def add_balance():
    session['balance'] = session.get('balance', 0.0) + 500.0
    return redirect(request.referrer)

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/products')
def index():
    search_query = request.args.get('search')
    products = get_products(search_query)
    if products is None:
        flash('Failed to connect to the API. Please try again later.', 'error')
        products = []
    return render_template('index.html', products=products)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = get_product(product_id)
    if product is None:
        flash('Failed to retrieve product details. Please try again later.', 'error')
        return render_template('product_detail.html', product={})
    return render_template('product_detail.html', product=product, get_status=get_status)

@app.route('/order/<int:product_id>', methods=['POST'])
def order(product_id):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)