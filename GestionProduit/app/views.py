from django.shortcuts import render
from .models import Product, Provider, Stock
from django.views.generic import *
from django.http import HttpResponse
from .forms import ProductForm, ProviderForm, StockForm
from django.shortcuts import redirect
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy

# Create your views here.

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# Product
class Products(ListView):
    model = Product
    template_name = 'product/products.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Liste des produits"
        products = self.get_queryset()
        for product in products:
            stock = Stock.objects.filter(product=product).first()
            if stock:
                product.price_ttc = product.price_ht * (1 + stock.rate / 100)
            else:
                product.price_ttc = product.price_ht

            providers = Stock.objects.filter(product=product)
            if providers:
                product.providers = [provider.provider for provider in providers]
                product.stock = sum([provider.quantity for provider in providers])
        
        context['products'] = products
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['title'] = "Détail du produit"
        stock = Stock.objects.filter(product=self.object).first()
        if stock:
            context['price_ttc'] = self.object.price_ht * (1 + stock.rate / 100)
        else:
            context['price_ttc'] = self.object.price_ht
        return context

class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/add.html'

    def form_valid(self, form: BaseModelForm):
        product = form.save()
        return redirect('product', product.id)

class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/update.html'

    def form_valid(self, form: BaseModelForm):
        product = form.save()
        return redirect('product', product.id)
    
    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modification du produit"
        return context

class ProductDelete(DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('products')
    

# Provider
class Providers(ListView):
    model = Provider
    template_name = 'provider/providers.html'
    context_object_name = 'providers'
    
    def get_queryset(self):
        return Provider.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Liste des fournisseurs"
        context['providers'] = Provider.objects.all()
        return context

class ProviderDetail(DetailView):
    model = Provider
    template_name = 'provider/provider.html'
    context_object_name = 'provider'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Détail du fournisseur"
        return context

class ProviderCreate(CreateView):
    model = Provider
    form_class = ProviderForm
    template_name = 'provider/add.html'

    def form_valid(self, form: BaseModelForm):
        provider = form.save()
        return redirect('provider', provider.id)

class ProviderUpdate(UpdateView):
    model = Provider
    form_class = ProviderForm
    template_name = 'provider/update.html'

    def form_valid(self, form: BaseModelForm):
        provider = form.save()
        return redirect('provider', provider.id)
    
    def get_context_data(self, **kwargs):
        context = super(ProviderUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modification du fournisseur"
        return context

class ProviderDelete(DeleteView):
    model = Provider
    template_name = 'provider/delete.html'
    success_url = reverse_lazy('providers')

# Stock

class Stocks(ListView):
    model = Stock
    template_name = 'stock/stocks.html'
    context_object_name = 'stocks'
    
    def get_queryset(self):
        return Stock.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Liste des stocks"
        context['stocks'] = Stock.objects.all()
        return context
    
class StockDetail(DetailView):
    model = Stock
    template_name = 'stock/stock.html'
    context_object_name = 'stock'

    def get_context_data(self, **kwargs):
        context = super(StockDetail, self).get_context_data(**kwargs)
        context['title'] = "Détail du stock"
        return context
    
class StockCreate(CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock/add.html'

    def form_valid(self, form: BaseModelForm):
        stock = form.save()
        return redirect('stock', stock.id)
    
class StockUpdate(UpdateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock/update.html'

    def form_valid(self, form: BaseModelForm):
        stock = form.save()
        return redirect('stock', stock.id)
    
    def get_context_data(self, **kwargs):
        context = super(StockUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modification du stock"
        return context
    
class StockDelete(DeleteView):
    model = Stock
    template_name = 'stock/delete.html'
    success_url = reverse_lazy('stocks')