from django.contrib import admin
from .models import RegistroPeso

@admin.register(RegistroPeso)
class RegistroPesoAdmin(admin.ModelAdmin):
    list_display = ('peso', 'unidad', 'fecha_registro', 'activo')
    list_filter = ('activo', 'fecha_registro')
    ordering = ('-fecha_registro',)