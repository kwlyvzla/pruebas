from django.db import models

class Empleado(models.Model):
    """Modelo para gestión de empleados con número generado automáticamente"""
    
    # ===== NÚMERO DE EMPLEADO (GENERADO AUTOMÁTICAMENTE) =====
    numero_empleado = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        verbose_name="Número de empleado"
    )
    
    # ===== DATOS PERSONALES =====
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre completo"
    )
    
    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Correo electrónico"
    )
    
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono"
    )
    
    direccion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Dirección"
    )
    
    # ===== DATOS LABORALES =====
    puesto = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Puesto"
    )
    
    departamento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Departamento"
    )
    
    fecha_ingreso = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de ingreso"
    )
    
    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Salario"
    )
    
    # ===== ESTADO Y FECHAS =====
    activo = models.BooleanField(
        default=True,
        verbose_name="Empleado activo"
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro"
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    
    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['numero_empleado']
    
    def __str__(self):
        return f"{self.numero_empleado} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        """Genera automáticamente el número de empleado al guardar"""
        if not self.numero_empleado:
            # Obtener el último número de empleado
            ultimo = Empleado.objects.order_by('-id').first()
            
            if ultimo and ultimo.numero_empleado:
                # Extraer el número del último empleado
                try:
                    ultimo_numero = int(ultimo.numero_empleado.replace('EMP', ''))
                    nuevo_numero = ultimo_numero + 1
                except ValueError:
                    nuevo_numero = 1
            else:
                nuevo_numero = 1
            
            # Formatear el número: EMP0001, EMP0002, etc.
            self.numero_empleado = f"EMP{nuevo_numero:04d}"
        
        super().save(*args, **kwargs)