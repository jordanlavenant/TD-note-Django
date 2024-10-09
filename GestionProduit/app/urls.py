from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    path('', views.index, name='index'),
    path("productsview", views.lesProduits, name='productsview'),
]

