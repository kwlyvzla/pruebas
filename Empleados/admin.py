from django.contrib import admin
from .models import Empleado

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('numero_empleado', 'nombre_completo', 'puesto', 'departamento', 'telefono', 'activo')
    search_fields = ('numero_empleado', 'nombre_completo', 'email')
    list_filter = ('activo', 'puesto', 'departamento')
    readonly_fields = ('numero_empleado', 'fecha_registro')