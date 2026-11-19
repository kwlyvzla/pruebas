from django.urls import path
from . import views

urlpatterns = [
    path('', views.bascula, name='bascula'),
    path('simular/', views.modo_simulacion, name='modo_simulacion'),
    path('real/', views.modo_real, name='modo_real'),
    path('simular/conectar/', views.conectar_simulador, name='conectar_simulador'),
    path('simular/desconectar/', views.desconectar_simulador, name='desconectar_simulador'),
    path('simular/registrar/', views.registrar_peso_simulado, name='registrar_peso_simulado'),
    path('real/registrar/', views.registrar_peso_real, name='registrar_peso_real'),
    path('eliminar/<int:id>/', views.eliminar_registro, name='eliminar_registro'),
    path('limpiar/', views.limpiar_registros, name='limpiar_registros'),
]