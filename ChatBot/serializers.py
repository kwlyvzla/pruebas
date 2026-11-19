from rest_framework import serializers
from .models import MensajeChat
from Asistencias.models import RegistroAsistencia


class MensajeChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeChat
        fields = ['id_mensaje', 'tipo', 'contenido', 'remitente', 'ubicacion', 'fecha_envio']
        read_only_fields = ['id_mensaje', 'fecha_envio']


class RegistroAsistenciaSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.nombre_completo', read_only=True)

    class Meta:
        model = RegistroAsistencia
        fields = [
            'id', 'empleado', 'empleado_nombre', 'fecha',
            'hora_entrada', 'hora_salida', 'estado',
            'observaciones', 'fecha_registro',
        ]
        read_only_fields = ['id', 'fecha_registro']
