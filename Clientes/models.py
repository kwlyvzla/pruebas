from django.db import models

class Cliente(models.Model):
    # Datos personales
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    direccion = models.TextField(verbose_name="Dirección")
    
    # Datos adicionales
    rfc = models.CharField(max_length=13, blank=True, null=True, verbose_name="RFC")
    empresa = models.CharField(max_length=100, blank=True, null=True, verbose_name="Empresa")
    
    # Fechas
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    # Estado
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']