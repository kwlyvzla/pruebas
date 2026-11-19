from django.db import models
from django.utils import timezone
import random

class MensajeChat(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('MENU', 'Menú'),
        ('RESPUESTA', 'Respuesta'),
    ]
    id_mensaje = models.CharField(max_length=50, unique=True, editable=False)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    contenido = models.TextField()
    remitente = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    fecha_envio = models.DateTimeField(default=timezone.now)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id_mensaje:
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            sufijo = str(random.randint(1000, 9999))
            self.id_mensaje = f"MSG-{timestamp}-{sufijo}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Mensaje de Chat"
        verbose_name_plural = "Mensajes de Chat"
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"{self.id_mensaje} - {self.tipo} ({self.remitente})"