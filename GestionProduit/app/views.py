from django.shortcuts import render
from .models import Product, Provider, Stock, Command, Order, Cart  
from django.views.generic import *
from django.http import HttpResponse
from .forms import ProductForm, ProviderForm, StockForm, CommandForm
from django.shortcuts import redirect
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

# Login
class ConnectView(LoginView):
    template_name = 'authentication/login.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            next_url = request.POST.get('next', request.GET.get('next', reverse_lazy('home')))
            return redirect(next_url)
        
        return render(request, self.template_name, {'error': 'Invalid credentials'})

    def get_context_data(self, **kwargs):
        context = super(ConnectView, self).get_context_data(**kwargs)
        context['title'] = "Connexion"
        return context

class DisconnectView(TemplateView):
    template_name = 'authentication/logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name, {'title': "Déconnexion"})

# Home
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_products(self):
        return Product.objects.all()

    def get_providers(self):
        return Provider.objects.all()

    def get_stocks(self):
        return Stock.objects.all()

    def get_commands(self):
        return Command.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['title'] = "Accueil"
        context['products'] = len(self.get_products())
        context['providers'] = len(self.get_providers())
        context['stocks'] = len(self.get_stocks())
        context['commands'] = len(self.get_commands())
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)

# Product
class Products(ListView):
    model = Product
    template_name = 'product/products.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        if (self.request.GET.get('search')):
            return Product.objects.filter(name__icontains=self.request.GET.get('search'))
        else: return Product.objects.all()

    def get_context_data(self, **kwargs):
        products = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['title'] = "Liste des produits"
        context['results'] = len(products)
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
        return get_object_or_404(Product, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['title'] = "Détail du produit"
        context['status'] = self.get_object().get_status()
        items = self.get_object().get_items()
        for item in items:
            item.price_ttc = item.get_price_ttc()
        context['items'] = items
        return context

@method_decorator(login_required, name='dispatch')
class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/add.html'

    def form_valid(self, form: BaseModelForm):
        product = form.save()
        return redirect('product', product.id)

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
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
        if (self.request.GET.get('search')):
            return Provider.objects.filter(name__icontains=self.request.GET.get('search'))
        else: return Provider.objects.all()

    def get_context_data(self, **kwargs):
        providers = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['title'] = "Liste des fournisseurs"
        context['results'] = len(providers)
        context['providers'] = providers
        return context

class ProviderDetail(DetailView):
    model = Provider
    template_name = 'provider/provider.html'
    context_object_name = 'provider'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Détail du fournisseur"
        stocks = self.get_object().get_stocks()
        for stock in stocks:
            stock.price_ttc = stock.product.price_ht * (1 + stock.rate / 100)
        context['stocks'] = stocks
        return context

@method_decorator(login_required, name='dispatch')
class ProviderCreate(CreateView):
    model = Provider
    form_class = ProviderForm
    template_name = 'provider/add.html'

    def form_valid(self, form: BaseModelForm):
        provider = form.save()
        return redirect('provider', provider.id)
    
@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
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
        search_query = self.request.GET.get('search')
        if search_query:
            return Stock.objects.filter(
                Q(product__name__icontains=search_query) | 
                Q(provider__name__icontains=search_query)
            )
        else: return Stock.objects.all()

    def get_context_data(self, **kwargs):
        stocks = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['title'] = "Liste des stocks"
        context["results"] = len(stocks)
        context['stocks'] = stocks
        return context
    
class StockDetail(DetailView):
    model = Stock
    template_name = 'stock/stock.html'
    context_object_name = 'stock'

    def get_context_data(self, **kwargs):
        context = super(StockDetail, self).get_context_data(**kwargs)
        context['title'] = "Détail du stock"
        return context
    
@method_decorator(login_required, name='dispatch')
class StockCreate(CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock/add.html'

    def form_valid(self, form: BaseModelForm):
        stock = form.save()
        return redirect('stock', stock.id)
    
@method_decorator(login_required, name='dispatch')
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
    
@method_decorator(login_required, name='dispatch')
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
        # search_query = self.request.GET.get('search')
        # if search_query:
        #     return Stock.objects.filter(
        #         Q(product__name__icontains=search_query) | 
        #         Q(provider__name__icontains=search_query)
        #     )
        # else: return Stock.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            currents = Command.objects.all().order_by('status').filter(
                Q(status__lt=2) &
                (Q(product__name__icontains=search_query) | Q(provider__name__icontains=search_query))
            )
            received = Command.objects.all().order_by('status').filter(
                Q(status=2) &
                (Q(product__name__icontains=search_query) | Q(provider__name__icontains=search_query))
            )
            return (currents, received)
        else:
            currents = Command.objects.all().order_by('status').filter(status__lt=2)
            received = Command.objects.all().order_by('status').filter(status=2)
            return (currents, received)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Liste des commandes"
        (currents, receiveds) = self.get_queryset()
        for current in currents:
            current.status = current.get_status() 
        for received in receiveds:
            received.status = received.get_status()

        context['currents'] = currents
        context['receiveds'] = receiveds
        context['results'] = len(receiveds) + len(currents)
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
    
@method_decorator(login_required, name='dispatch')
class CommandCreate(CreateView):
    model = Command
    form_class = CommandForm
    template_name = 'command/add.html'

    def form_valid(self, form: BaseModelForm):
        command = form.save()
        return redirect('command', command.id)
    
@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class CommandDelete(DeleteView):
    model = Command
    template_name = 'command/delete.html'
    success_url = reverse_lazy('commands')

from rest_framework import permissions, viewsets, filters
from .serializers import ProductSerializer, ProviderSerializer, StockSerializer, CommandSerializer, OrderSerializer, CartSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'provider']
    search_fields = ['product__name', 'provider__name']

class CommandViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows commands to be viewed or edited.
    """
    queryset = Command.objects.all().order_by('date')
    serializer_class = CommandSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows carts to be viewed or edited.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']