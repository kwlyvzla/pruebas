from django.contrib import admin
from .models import Empleado

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('numero_empleado', 'nombre_completo', 'puesto', 'activo', 'fecha_contratacion')
    search_fields = ('nombre', 'apellidos', 'numero_empleado', 'curp', 'rfc')
    list_filter = ('activo', 'puesto', 'fecha_contratacion')
    ordering = ('apellidos', 'nombre')
    list_editable = ('puesto', 'activo')
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')
    
    fieldsets = (
        ('📋 Datos Personales', {
            'fields': ('nombre', 'apellidos', 'curp', 'rfc')
        }),
        ('📞 Contacto', {
            'fields': ('celular', 'direccion')
        }),
        ('💼 Datos Laborales', {
            'fields': ('puesto', 'fecha_contratacion', 'salario', 'nss', 'numero_empleado')
        }),
        ('📅 Estado', {
            'fields': ('activo', 'fecha_registro', 'fecha_actualizacion')
        }),
    )

admin.site.register(Empleado, EmpleadoAdmin)