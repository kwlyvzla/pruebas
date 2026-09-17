from django.db import models

class Empleado(models.Model):
    # ===== DATOS PERSONALES =====
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    curp = models.CharField(max_length=18, blank=True, null=True, verbose_name="CURP")
    rfc = models.CharField(max_length=13, blank=True, null=True, verbose_name="RFC")
    
    # ===== CONTACTO =====
    ## email = models.EmailField(max_length=100, blank=True, null=True, verbose_name="Correo electrónico")
    celular = models.CharField(max_length=20, blank=True, null=True, verbose_name="Celular")
    direccion = models.TextField(verbose_name="Dirección")
    
    # ===== DATOS LABORALES =====
    PUESTOS = [
        ('ADMIN', 'Administrador'),
        ('GERENTE', 'Gerente'),
        ('SUPERVISOR', 'Supervisor'),
        ('VENDEDOR', 'Vendedor'),
        ('ALMACEN', 'Almacenista'),
        ('CONDUCTOR', 'Conductor'),
        ('OPERADOR', 'Operador'),
        ('SOPORTE', 'Soporte Técnico'),
        ('OTRO', 'Otro'),
    ]
    
    puesto = models.CharField(
        max_length=20,
        choices=PUESTOS,
        default='OTRO',
        verbose_name="Puesto"
    )
    
    fecha_contratacion = models.DateField(verbose_name="Fecha de contratación")
    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Salario"
    )
    
    # ===== DATOS DE IDENTIFICACIÓN =====
    nss = models.CharField(max_length=20, blank=True, null=True, verbose_name="NSS")
    numero_empleado = models.CharField(max_length=20, unique=True, verbose_name="Número de empleado")
    
    # ===== ESTADO =====
    activo = models.BooleanField(default=True, verbose_name="Empleado activo")
    
    # ===== FECHAS =====
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    # ===== METADATOS =====
    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['apellidos', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.numero_empleado})"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"