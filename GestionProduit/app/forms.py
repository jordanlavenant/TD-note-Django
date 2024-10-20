from django import forms
from .models import Product, Provider, Stock, Command

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = '__all__'
        exclude = ('status', 'date')