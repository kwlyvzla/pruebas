from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'proveedor', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo', 'proveedor')