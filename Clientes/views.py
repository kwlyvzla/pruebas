from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente

def lista_clientes(request):
    """Mostrar todos los clientes"""
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'Clientes/lista.html', {'clientes': clientes})

def agregar_cliente(request):
    """Agregar un nuevo cliente"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        rfc = request.POST.get('rfc')
        empresa = request.POST.get('empresa')
        activo = request.POST.get('activo') == 'on'
        
        # Validar datos obligatorios
        if nombre and email and telefono and direccion:
            Cliente.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                rfc=rfc,
                empresa=empresa,
                activo=activo
            )
            return redirect('lista_clientes')
    
    return render(request, 'Clientes/agregar.html')

def editar_cliente(request, id):
    """Editar un cliente existente"""
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        rfc = request.POST.get('rfc')
        empresa = request.POST.get('empresa')
        activo = request.POST.get('activo') == 'on'
        
        if nombre and email and telefono and direccion:
            cliente.nombre = nombre
            cliente.email = email
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.rfc = rfc
            cliente.empresa = empresa
            cliente.activo = activo
            cliente.save()
            return redirect('lista_clientes')
    
    return render(request, 'Clientes/editar.html', {'cliente': cliente})

def eliminar_cliente(request, id):
    """Eliminar un cliente (con confirmación)"""
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    
    return render(request, 'Clientes/eliminar.html', {'cliente': cliente})