from django.shortcuts import render, redirect
from .models import Proveedores

def lista_proveedores(request):
    proveedores = Proveedores.objects.all().order_by('nombre')
    return render(request, 'proveedores/lista.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        
        if nombre and direccion:
            Proveedores.objects.create(nombre=nombre, direccion=direccion)
            return redirect('lista')
    
    return render(request, 'proveedores/agregar.html')
