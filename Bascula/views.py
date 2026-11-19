from django.shortcuts import render, redirect, get_object_or_404
from .models import RegistroPeso
from .usb_connector import simulador

def bascula(request):
    registros = RegistroPeso.objects.all()[:100]
    return render(request, 'Bascula/bascula.html', {'registros': registros, 'seccion': 'principal'})

def modo_simulacion(request):
    registros = RegistroPeso.objects.all()[:100]
    peso_actual = simulador.obtener_peso() if simulador.is_connected else None
    return render(request, 'Bascula/simulacion.html', {
        'registros': registros,
        'simulador_activo': simulador.is_connected,
        'peso_actual': peso_actual,
        'seccion': 'simulacion'
    })

def modo_real(request):
    registros = RegistroPeso.objects.all()[:100]
    return render(request, 'Bascula/real.html', {'registros': registros, 'seccion': 'real'})

def conectar_simulador(request):
    if request.method == 'POST':
        simulador.conectar()
        return redirect('modo_simulacion')
    return redirect('modo_simulacion')

def desconectar_simulador(request):
    if request.method == 'POST':
        simulador.desconectar()
        return redirect('modo_simulacion')
    return redirect('modo_simulacion')

def registrar_peso_simulado(request):
    if request.method == 'POST':
        peso = request.POST.get('peso')
        if peso:
            try:
                peso = float(peso)
                if peso > 0:
                    RegistroPeso.objects.create(peso=peso)
            except ValueError:
                pass
    return redirect('modo_simulacion')

def registrar_peso_real(request):
    if request.method == 'POST':
        peso = request.POST.get('peso')
        if peso:
            try:
                peso = float(peso)
                if peso > 0:
                    RegistroPeso.objects.create(peso=peso)
            except ValueError:
                pass
    return redirect('modo_real')

def eliminar_registro(request, id):
    registro = get_object_or_404(RegistroPeso, id=id)
    if request.method == 'POST':
        registro.delete()
        return redirect('bascula')
    return render(request, 'Bascula/eliminar.html', {'registro': registro})

def limpiar_registros(request):
    if request.method == 'POST':
        RegistroPeso.objects.all().delete()
        return redirect('bascula')
    return render(request, 'Bascula/limpiar.html')