from django.shortcuts import render, redirect, get_object_or_404
from .models import RegistroPeso

def lista_pesos(request):
    """Mostrar todos los registros de peso"""
    registros = RegistroPeso.objects.all()[:50]  # Últimos 50 registros
    return render(request, 'Bascula/lista.html', {'registros': registros})

def bascula(request):
    """Vista principal de la báscula con conexión USB"""
    registros = RegistroPeso.objects.all()[:100]  # Últimos 100 registros
    return render(request, 'Bascula/bascula.html', {'registros': registros})

def eliminar_registro(request, id):
    """Eliminar un registro de peso"""
    registro = get_object_or_404(RegistroPeso, id=id)
    
    if request.method == 'POST':
        registro.delete()
        return redirect('bascula')
    
    return render(request, 'Bascula/eliminar.html', {'registro': registro})

def limpiar_registros(request):
    """Eliminar todos los registros (con confirmación)"""
    if request.method == 'POST':
        RegistroPeso.objects.all().delete()
        return redirect('bascula')
    
    return render(request, 'Bascula/limpiar.html')