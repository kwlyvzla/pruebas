from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(unique=True, verbose_name="Email")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    direccion = models.TextField(verbose_name="Dirección")
    rfc = models.CharField(max_length=13, blank=True, null=True, verbose_name="RFC")
    empresa = models.CharField(max_length=100, blank=True, null=True, verbose_name="Empresa")
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre