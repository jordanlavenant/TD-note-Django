from django.contrib import admin
from .models import Product, Provider, ProductProvider

# Register your models here.
admin.site.register(Product)
admin.site.register(Provider)
admin.site.register(ProductProvider)