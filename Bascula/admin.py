from django.contrib import admin
from .models import RegistroPeso

class RegistroPesoAdmin(admin.ModelAdmin):
    list_display = ('peso', 'unidad', 'fecha_registro', 'activo')
    list_filter = ('activo', 'unidad', 'fecha_registro')
    search_fields = ('peso', 'observaciones')
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')
    ordering = ('-fecha_registro',)

admin.site.register(RegistroPeso, RegistroPesoAdmin)