from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.bascula, name='bascula'),
    
    # Modos
    path('simular/', views.modo_simulacion, name='modo_simulacion'),
    path('real/', views.modo_real, name='modo_real'),
    
    # Registros
    path('lista/', views.lista_pesos, name='lista_pesos'),
    path('eliminar/<int:id>/', views.eliminar_registro, name='eliminar_registro'),
    path('limpiar/', views.limpiar_registros, name='limpiar_registros'),
    
    # Simulación
    path('simular/conectar/', views.conectar_simulador, name='conectar_simulador'),
    path('simular/desconectar/', views.desconectar_simulador, name='desconectar_simulador'),
    path('simular/registrar/', views.registrar_peso_simulado, name='registrar_peso_simulado'),
    
    # Báscula Real
    path('real/conectar/', views.conectar_usb, name='conectar_usb'),
    path('real/desconectar/', views.desconectar_usb, name='desconectar_usb'),
    path('real/registrar/', views.registrar_peso_real, name='registrar_peso_real'),
]