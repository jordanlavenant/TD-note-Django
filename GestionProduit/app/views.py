from django.shortcuts import render
from .models import Product, ProductItem, Provider, Stock, Command
from django.views.generic import *
from django.http import HttpResponse
from .forms import ProductForm, ProviderForm, StockForm, CommandForm
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
                product.providers = len(providers)
                product.stock = sum([provider.quantity for provider in providers])
        
        context['products'] = products
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product.html'
    context_object_name = 'product'

    def get_object(self):
        return Product.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['title'] = "Détail du produit"
        items = self.get_object().product_items.all()
        for item in items:
            item.price_ttc = item.get_price_ttc()
        context['items'] = items
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

# Command
class Commands(ListView):
    model = Command
    template_name = 'command/commands.html'
    context_object_name = 'commands'
    
    def get_queryset(self):
        return Command.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Liste des commandes"
        commands = self.get_queryset()
        for command in commands:
            command.status = command.get_status()
        context['commands'] = commands
        return context
    
class CommandDetail(DetailView):
    model = Command
    template_name = 'command/command.html'
    context_object_name = 'command'

    def get_context_data(self, **kwargs):
        context = super(CommandDetail, self).get_context_data(**kwargs)
        context['title'] = "Détail de la commande"
        context['status'] = self.get_object().get_status()
        return context
    
class CommandCreate(CreateView):
    model = Command
    form_class = CommandForm
    template_name = 'command/add.html'

    def form_valid(self, form: BaseModelForm):
        command = form.save()
        return redirect('command', command.id)
    
class CommandUpdate(UpdateView):
    model = Command
    form_class = CommandForm
    template_name = 'command/update.html'

    def form_valid(self, form: BaseModelForm):
        command = form.save()
        return redirect('command', command.id)
    
    def get_context_data(self, **kwargs):
        context = super(CommandUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modification de la commande"
        return context
    
class CommandDelete(DeleteView):
    model = Command
    template_name = 'command/delete.html'
    success_url = reverse_lazy('commands')


from rest_framework import permissions, viewsets
from .serializers import ProductSerializer, ProviderSerializer, StockSerializer, CommandSerializer, ProductItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Provider.objects.all().order_by('name')
    serializer_class = ProviderSerializer

class StockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stocks to be viewed or edited.
    """
    queryset = Stock.objects.all().order_by('product')
    serializer_class = StockSerializer

class CommandViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows commands to be viewed or edited.
    """
    queryset = Command.objects.all().order_by('date')
    serializer_class = CommandSerializer

class ProductItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product items to be viewed or edited.
    """
    queryset = ProductItem.objects.all().order_by('product')
    serializer_class = ProductItemSerializer