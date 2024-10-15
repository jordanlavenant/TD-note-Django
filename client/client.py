import requests

BASE_URL = 'http://localhost:8000/api/'

def get_products():
    response = requests.get(f'{BASE_URL}products/')
    return response.json()

def get_product(product_id):
    response = requests.get(f'{BASE_URL}products/{product_id}/')
    return response.json()

def create_product(data):
    response = requests.post(f'{BASE_URL}products/', data=data)
    return response.json()

def update_product(product_id, data):
    response = requests.put(f'{BASE_URL}products/{product_id}/', data=data)
    return response.json()

def delete_product(product_id):
    response = requests.delete(f'{BASE_URL}products/{product_id}/')
    return response.status_code