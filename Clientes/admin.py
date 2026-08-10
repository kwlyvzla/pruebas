from django.contrib import admin
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
    # Columnas que se muestran en la lista
    list_display = ('nombre', 'email', 'telefono', 'empresa', 'activo', 'fecha_registro')
    
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'email', 'telefono', 'rfc', 'empresa')
    
    # Campos que se pueden filtrar
    list_filter = ('activo', 'empresa', 'fecha_registro')
    
    # Ordenamiento
    ordering = ('nombre',)
    
    # Campos que se pueden editar directamente desde la lista
    list_editable = ('telefono', 'activo')
    
    # Campos de solo lectura
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')

admin.site.register(Cliente, ClienteAdmin)