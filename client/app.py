from flask import Flask, redirect, render_template, flash, request, session, url_for
from client import get_products, get_product, get_stock, get_provider, add_order
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
def index():
    return redirect(url_for('products'))

@app.route('/products')
def products():
    search_query = request.args.get('search')
    products = get_products(search_query)
    if products is None:
        flash('Failed to connect to the API. Please try again later.', 'error')
        products = []
    return render_template('products.html', products=products)

@app.route('/products/<int:product_id>')
def product(product_id):
    product = get_product(product_id)
    if product is None:
        flash('Failed to retrieve product details. Please try again later.', 'error')
        return render_template('product.html', product={})
    stocks = get_stock(product_id)
    return render_template(
        'product.html', 
        product=product, 
        get_status=get_status,
        get_provider=get_provider,
        stocks=stocks
    )

@app.route('/order/<int:product_id>/<int:provider_id>/')
def order(product_id, provider_id):
    default_user = 1
    try:
        add_order(product_id, provider_id, 1, default_user)
        flash('Order placed successfully!', 'success')
    except requests.exceptions.RequestException:
        flash('Failed to place order. Please try again later.', 'error')
    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(debug=True)