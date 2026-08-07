from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_proveedores, name='lista'),  # ← lista_proveedores (minúscula)
    path('agregar/', views.agregar_proveedor, name='agregar'),
    path('editar/<int:id>/', views.editar_proveedor, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar'),
]