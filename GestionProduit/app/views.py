from django.shortcuts import render
from .models import Product

# Create your views here.

from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def lesProduits(request):
    products = Product.objects.all()
    print(products)
    return render(request, 'listProducts.html', {'products': products}) 