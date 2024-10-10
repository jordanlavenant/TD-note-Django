# from django.contrib.auth.models import Group, User
from .models import Product, Stock, ProductItem, Provider, Command
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = '__all__'

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = '__all__'