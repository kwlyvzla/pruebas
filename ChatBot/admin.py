from django.contrib import admin
from .models import MensajeChat
from Asistencias.models import RegistroAsistencia


@admin.register(MensajeChat)
class MensajeChatAdmin(admin.ModelAdmin):
    list_display = ('id_mensaje', 'tipo', 'remitente', 'fecha_envio', 'ubicacion')
    list_filter = ('tipo', 'fecha_envio')
    search_fields = ('id_mensaje', 'remitente', 'contenido')
    readonly_fields = ('id_mensaje', 'fecha_registro')
    ordering = ('-fecha_envio',)


@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = [
        'empleado',
        'fecha',
        'hora_entrada',
        'hora_salida',
        'estado',
        'fecha_registro',
    ]
    list_filter = ['estado', 'fecha', 'empleado__departamento']
    search_fields = ['empleado__nombre_completo', 'empleado__numero_empleado']
    date_hierarchy = 'fecha'
    ordering = ['-fecha', 'empleado__numero_empleado']
