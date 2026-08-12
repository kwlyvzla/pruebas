from django.urls import path
from . import views

urlpatterns = [
    path('', views.bascula, name='bascula'),
    path('lista/', views.lista_pesos, name='lista_pesos'),
    path('eliminar/<int:id>/', views.eliminar_registro, name='eliminar_registro'),
    path('limpiar/', views.limpiar_registros, name='limpiar_registros'),
]