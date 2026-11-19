from django.db import models
from Empleados.models import Empleado


class RegistroAsistencia(models.Model):
    ESTADOS = [
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente'),
        ('RETARDO', 'Retardo'),
        ('PERMISO', 'Permiso'),
    ]

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        verbose_name="Empleado"
    )
    fecha = models.DateField(verbose_name="Fecha")
    hora_entrada = models.TimeField(
        verbose_name="Hora de entrada",
        blank=True,
        null=True
    )
    hora_salida = models.TimeField(
        verbose_name="Hora de salida",
        blank=True,
        null=True
    )
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='PRESENTE',
        verbose_name="Estado"
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de asistencia"
        verbose_name_plural = "Registros de asistencia"
        ordering = ['-fecha', 'empleado__numero_empleado']
        unique_together = ['empleado', 'fecha']

    def __str__(self):
        return f"{self.empleado.numero_empleado} - {self.fecha} ({self.get_estado_display()})"
