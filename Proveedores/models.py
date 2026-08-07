from django.db import models

class Proveedor(models.Model):  # ← SINGULAR, sin "es"
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    
    def __str__(self):
        return self.nombre