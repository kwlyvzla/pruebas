from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rfc', 'email', 'activo', 'fecha_registro')
    search_fields = ('nombre', 'rfc', 'email')
    list_filter = ('activo',)