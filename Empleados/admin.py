from django.contrib import admin
from .models import Empleado

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('numero_empleado', 'nombre', 'puesto', 'departamento', 'activo', 'fecha_ingreso')
    search_fields = ('numero_empleado', 'nombre', 'email', 'puesto', 'departamento')
    list_filter = ('activo', 'departamento', 'fecha_ingreso')
    ordering = ('numero_empleado',)
    list_editable = ('puesto', 'departamento', 'activo')
    readonly_fields = ('numero_empleado', 'fecha_registro', 'fecha_actualizacion')
    
    fieldsets = (
        ('📋 Número de Empleado', {
            'fields': ('numero_empleado',)
        }),
        ('👤 Datos Personales', {
            'fields': ('nombre', 'email', 'telefono', 'direccion')
        }),
        ('💼 Datos Laborales', {
            'fields': ('puesto', 'departamento', 'fecha_ingreso', 'salario')
        }),
        ('📅 Estado', {
            'fields': ('activo', 'fecha_registro', 'fecha_actualizacion')
        }),
    )

admin.site.register(Empleado, EmpleadoAdmin)