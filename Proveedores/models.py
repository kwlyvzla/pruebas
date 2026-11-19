from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    rfc = models.CharField(max_length=13, blank=True, null=True, verbose_name="RFC")
    direccion = models.TextField(verbose_name="Dirección")
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name="Email")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre