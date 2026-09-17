from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_empleados, name='lista_empleados'),
    path('agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
]