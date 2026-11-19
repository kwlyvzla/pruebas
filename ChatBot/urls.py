from django.urls import path
from . import views

urlpatterns = [
    # --- Chat Bot ---
    path('', views.chat_view, name='chat_view'),
    path('api/seleccionar-empleado/', views.seleccionar_empleado, name='seleccionar_empleado'),
    path('api/limpiar-sesion/', views.limpiar_sesion_chat, name='limpiar_sesion_chat'),
    path('api/mensaje/', views.procesar_mensaje, name='procesar_mensaje'),
    path('api/guardar/', views.guardar_mensaje, name='guardar_mensaje'),
    path('webhook/', views.recibir_webhook, name='recibir_webhook'),

    # --- Registro de Asistencia ---
    path('asistencias/', views.lista_asistencias, name='chat_asistencias'),
    path('asistencias/agregar/', views.agregar_asistencia, name='chat_agregar_asistencia'),
    path('asistencias/editar/<int:id>/', views.editar_asistencia, name='chat_editar_asistencia'),
    path('asistencias/eliminar/<int:id>/', views.eliminar_asistencia, name='chat_eliminar_asistencia'),

    # --- Kiosco de Checada ---
    path('kiosco/', views.kiosco_view, name='chat_kiosco'),
    path('kiosco/api/checar/', views.kiosco_checar, name='kiosco_checar'),
]
