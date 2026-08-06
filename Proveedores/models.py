from django.db import models

class Proveedores(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(max_length=100)

def _str_(self):
    return self.nombre
