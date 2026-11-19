from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_asistencias, name='lista_asistencias'),
    path('agregar/', views.agregar_asistencia, name='agregar_asistencia'),
    path('editar/<int:id>/', views.editar_asistencia, name='editar_asistencia'),
    path('eliminar/<int:id>/', views.eliminar_asistencia, name='eliminar_asistencia'),
]
