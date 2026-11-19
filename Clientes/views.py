from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente

def lista_clientes(request):
    clientes = Cliente.objects.filter(activo=True).order_by('nombre')
    return render(request, 'Clientes/lista.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre=request.POST.get('nombre'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion'),
            rfc=request.POST.get('rfc') or '',
            empresa=request.POST.get('empresa') or '',
            activo=request.POST.get('activo') == 'on',
        )
        return redirect('lista_clientes')
    return render(request, 'Clientes/agregar.html')

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')
        cliente.rfc = request.POST.get('rfc')
        cliente.empresa = request.POST.get('empresa')
        cliente.activo = request.POST.get('activo') == 'on'
        cliente.save()
        return redirect('lista_clientes')
    return render(request, 'Clientes/editar.html', {'cliente': cliente})

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'Clientes/eliminar.html', {'cliente': cliente})