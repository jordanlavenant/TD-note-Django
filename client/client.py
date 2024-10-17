import requests

BASE_URL = 'http://localhost:8000/api/'

def get_products(search_query=None):
    params = {'search': search_query} if search_query else {}
    response = requests.get(f'{BASE_URL}products/', params=params)
    return response.json()

def get_product(product_id):
    response = requests.get(f'{BASE_URL}products/{product_id}/')
    return response.json()

def get_stock(product_id):
    response = requests.get(f'{BASE_URL}stocks/?product={product_id}')
    return response.json()

def get_provider(provider_id):
    response = requests.get(f'{BASE_URL}providers/{provider_id}/')
    return response.json()

def add_order(product, provider, quantity, user):
    response = requests.post(f'{BASE_URL}orders/', json={
        'product': product,
        'provider': provider,
        'quantity': quantity,
        'user': user
    })
    print(response.json())
    return response.json()