from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor

def lista_proveedores(request):
    proveedores = Proveedor.objects.filter(activo=True).order_by('nombre')
    return render(request, 'Proveedores/lista.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nombre=request.POST.get('nombre'),
            rfc=request.POST.get('rfc') or '',
            direccion=request.POST.get('direccion'),
            email=request.POST.get('email') or '',
            activo=request.POST.get('activo') == 'on',
        )
        return redirect('lista_proveedores')
    return render(request, 'Proveedores/agregar.html')

def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.nombre = request.POST.get('nombre')
        proveedor.rfc = request.POST.get('rfc')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.email = request.POST.get('email')
        proveedor.activo = request.POST.get('activo') == 'on'
        proveedor.save()
        return redirect('lista_proveedores')
    return render(request, 'Proveedores/editar.html', {'proveedor': proveedor})

def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('lista_proveedores')
    return render(request, 'Proveedores/eliminar.html', {'proveedor': proveedor})