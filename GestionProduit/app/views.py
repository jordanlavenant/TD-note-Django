from django.shortcuts import render
from .models import Product, Provider, ProductProvider
from django.views.generic import *
from django.http import HttpResponse
from .forms import ProductForm, ProviderForm
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
        context['products'] = Product.objects.all()
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['title'] = "Détail du produit"
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

class ProviderUpdate(UpdateView):
    pass

class ProviderDelete(DeleteView):
    pass