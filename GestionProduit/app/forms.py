from django import forms
from .models import Product, Provider, ProductProvider

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ('price_ttc', 'status')

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'