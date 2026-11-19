from django.db import models

class RegistroPeso(models.Model):
    peso = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Peso (kg)")
    unidad = models.CharField(max_length=10, default="kg")
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Registro de peso"
        verbose_name_plural = "Registros de pesos"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.peso} kg - {self.fecha_registro.strftime('%d/%m/%Y %H:%M')}"