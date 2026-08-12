from django.db import models

class RegistroPeso(models.Model):
    peso = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Peso (kg)")
    unidad = models.CharField(max_length=10, default="kg", verbose_name="Unidad")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    activo = models.BooleanField(default=True, verbose_name="Registro activo")
    
    def __str__(self):
        return f"{self.peso} kg - {self.fecha_registro.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        verbose_name = "Registro de peso"
        verbose_name_plural = "Registros de pesos"
        ordering = ['-fecha_registro']