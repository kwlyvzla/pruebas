from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_proveedores, name='lista'),
    path('agregar/', views.agregar_proveedor, name='agregar'),
]