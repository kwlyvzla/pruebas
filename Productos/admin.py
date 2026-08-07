from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    # Columnas que se muestran en la lista
    list_display = ('nombre', 'precio', 'stock', 'proveedor', 'activo', 'fecha_creacion')
    
    # Campos que se pueden filtrar
    list_filter = ('activo', 'proveedor', 'fecha_creacion')
    
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'descripcion')
    
    # Ordenamiento
    ordering = ('nombre',)
    
    # Campos que se pueden editar directamente desde la lista
    list_editable = ('precio', 'stock', 'activo')
    
    # Agregar campos de solo lectura
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

admin.site.register(Producto, ProductoAdmin)