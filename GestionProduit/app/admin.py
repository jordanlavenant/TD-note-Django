from django.contrib import admin
from .models import Product, ProductItem, Provider, Stock, Command  

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductItem)
admin.site.register(Provider)
admin.site.register(Stock)
admin.site.register(Command)
