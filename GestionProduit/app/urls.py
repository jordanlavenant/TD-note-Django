from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    # path('', views.index, name='index'),


    # Product
    path("products", views.Products.as_view(), name='products'),
    path("products/<pk>", views.ProductDetail.as_view(), name='product'),
    path("products/add/", views.ProductCreate.as_view(), name='product-add'),
    path("products/<pk>/update/", views.ProductUpdate.as_view(), name='product-update'),
    path("products/<pk>/delete/", views.ProductDelete.as_view(), name='product-delete'),

    # Provider
    path("providers", views.Providers.as_view(), name='providers'),
    path("providers/<pk>", views.ProviderDetail.as_view(), name='provider'),
    path("providers/add/", views.ProviderCreate.as_view(), name='provider-add'),
    path("providers/<pk>/update/", views.ProviderUpdate.as_view(), name='provider-update'),
    path("providers/<pk>/delete/", views.ProviderDelete.as_view(), name='provider-delete'),

    # Stock
    path("stocks", views.Stocks.as_view(), name='stocks'),
    path("stocks/<pk>", views.StockDetail.as_view(), name='stock'),
    path("stocks/add/", views.StockCreate.as_view(), name='stock-add'),
    path("stocks/<pk>/update/", views.StockUpdate.as_view(), name='stock-update'),
    path("stocks/<pk>/delete/", views.StockDelete.as_view(), name='stock-delete'),
]

