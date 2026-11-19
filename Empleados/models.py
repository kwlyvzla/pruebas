from django.db import models
from django.utils import timezone

class Empleado(models.Model):
    numero_empleado = models.CharField(max_length=20, unique=True, editable=False)
    nombre_completo = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    direccion = models.TextField()
    foto = models.ImageField(upload_to='empleados/fotos/', blank=True, null=True)

    PUESTOS = [
        ('GERENTE', 'Gerente'), ('SUPERVISOR', 'Supervisor'),
        ('ADMINISTRATIVO', 'Administrativo'), ('OPERATIVO', 'Operativo'),
        ('VENTAS', 'Ventas'), ('ALMACEN', 'Almacén'), ('OTRO', 'Otro'),
    ]
    puesto = models.CharField(max_length=20, choices=PUESTOS, default='OPERATIVO')

    DEPARTAMENTOS = [
        ('ADMINISTRACION', 'Administración'), ('VENTAS', 'Ventas'),
        ('PRODUCCION', 'Producción'), ('ALMACEN', 'Almacén'),
        ('RECURSOS_HUMANOS', 'Recursos Humanos'), ('CONTABILIDAD', 'Contabilidad'),
        ('SISTEMAS', 'Sistemas'), ('OTRO', 'Otro'),
    ]
    departamento = models.CharField(max_length=20, choices=DEPARTAMENTOS, default='OTRO')

    fecha_ingreso = models.DateField(default=timezone.now)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['numero_empleado']

    def save(self, *args, **kwargs):
        if not self.numero_empleado:
            ultimo = Empleado.objects.order_by('-id').first()
            if ultimo and ultimo.numero_empleado:
                try:
                    num = int(ultimo.numero_empleado.replace('EMP', '')) + 1
                except ValueError:
                    num = 1
            else:
                num = 1
            self.numero_empleado = f"EMP{num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_empleado} - {self.nombre_completo}"