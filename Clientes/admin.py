from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'empresa', 'activo')
    search_fields = ('nombre', 'email', 'empresa')
    list_filter = ('activo',)