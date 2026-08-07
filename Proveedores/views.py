from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor  # ← Modelo en SINGULAR

def lista_proveedores(request):
    proveedores = Proveedor.objects.all().order_by('nombre')  # ← Proveedor (sin "es")
    return render(request, 'Proveedores/lista.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        
        if nombre and direccion:
            Proveedor.objects.create(nombre=nombre, direccion=direccion)  # ← Proveedor
            return redirect('lista')
    
    return render(request, 'Proveedores/agregar.html')

def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)  # ← Proveedor
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        
        if nombre and direccion:
            proveedor.nombre = nombre
            proveedor.direccion = direccion
            proveedor.save()
            return redirect('lista')
    
    return render(request, 'Proveedores/editar.html', {'proveedor': proveedor})

def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)  # ← Proveedor
    
    if request.method == 'POST':
        proveedor.delete()
        return redirect('lista')
    
    return render(request, 'Proveedores/eliminar.html', {'proveedor': proveedor})