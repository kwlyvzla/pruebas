from django.shortcuts import render, redirect, get_object_or_404
from .models import RegistroPeso
from .usb_connector import simulador

def bascula(request):
    """Página principal de la báscula con pestañas"""
    registros = RegistroPeso.objects.all()[:100]
    return render(request, 'Bascula/bascula.html', {
        'registros': registros,
        'seccion': 'principal'
    })

def modo_simulacion(request):
    """Modo simulacion - Registro automatico de pesos"""
    registros = RegistroPeso.objects.all()[:100]
    
    # Si el simulador esta activo, obtener el ultimo peso
    peso_actual = None
    if simulador.is_connected:
        peso_actual = simulador.obtener_peso()
    
    # Si el simulador esta activo, recargar automaticamente
    if simulador.is_connected:
        # Usar un header para que el navegador recargue cada 3 segundos
        response = render(request, 'Bascula/simulacion.html', {
            'registros': registros,
            'simulador_activo': simulador.is_connected,
            'peso_actual': peso_actual,
            'seccion': 'simulacion'
        })
        # Agregar meta refresh para recargar automaticamente
        response['Refresh'] = '3'
        return response
    
    return render(request, 'Bascula/simulacion.html', {
        'registros': registros,
        'simulador_activo': simulador.is_connected,
        'peso_actual': peso_actual,
        'seccion': 'simulacion'
    })

def modo_real(request):
    """Modo báscula real - Conexión USB"""
    registros = RegistroPeso.objects.all()[:100]
    return render(request, 'Bascula/real.html', {
        'registros': registros,
        'seccion': 'real'
    })

def lista_pesos(request):
    """Mostrar todos los registros de peso"""
    registros = RegistroPeso.objects.all()[:50]
    return render(request, 'Bascula/lista.html', {'registros': registros})

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

# ===== FUNCIONES PARA SIMULACIÓN =====
def conectar_simulador(request):
    """Conectar el simulador de báscula"""
    if request.method == 'POST':
        success, mensaje = simulador.conectar()
        return redirect('modo_simulacion')
    return redirect('modo_simulacion')

def desconectar_simulador(request):
    """Desconectar el simulador de báscula"""
    if request.method == 'POST':
        success, mensaje = simulador.desconectar()
        return redirect('modo_simulacion')
    return redirect('modo_simulacion')

def registrar_peso_simulado(request):
    """Registrar un peso manualmente en modo simulación"""
    if request.method == 'POST':
        peso = request.POST.get('peso')
        if peso:
            try:
                peso = float(peso)
                if peso > 0:
                    RegistroPeso.objects.create(peso=peso)
                    return redirect('modo_simulacion')
            except ValueError:
                pass
    return redirect('modo_simulacion')

# ===== FUNCIONES PARA BÁSCULA REAL =====
def conectar_usb(request):
    """Conectar báscula real por USB"""
    # Aquí irá la lógica de conexión USB real
    return redirect('modo_real')

def desconectar_usb(request):
    """Desconectar báscula real"""
    # Aquí irá la lógica de desconexión USB real
    return redirect('modo_real')

def registrar_peso_real(request):
    """Registrar peso desde báscula real"""
    if request.method == 'POST':
        peso = request.POST.get('peso')
        if peso:
            try:
                peso = float(peso)
                if peso > 0:
                    RegistroPeso.objects.create(peso=peso)
                    return redirect('modo_real')
            except ValueError:
                pass
    return redirect('modo_real')