from django import forms
from .models import Product, Provider, Stock

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ('price_ttc', 'status')

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'