from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from Proveedores.models import Proveedor

def lista_productos(request):
    productos = Producto.objects.filter(activo=True).order_by('nombre')
    return render(request, 'Productos/lista.html', {'productos': productos})

def agregar_producto(request):
    proveedores = Proveedor.objects.filter(activo=True)
    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion') or '',
            precio=request.POST.get('precio'),
            stock=request.POST.get('stock') or 0,
            proveedor_id=request.POST.get('proveedor') or None,
            activo=request.POST.get('activo') == 'on',
        )
        return redirect('lista_productos')
    return render(request, 'Productos/agregar.html', {'proveedores': proveedores})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    proveedores = Proveedor.objects.filter(activo=True)
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock') or 0
        producto.proveedor_id = request.POST.get('proveedor') or None
        producto.activo = request.POST.get('activo') == 'on'
        producto.save()
        return redirect('lista_productos')
    return render(request, 'Productos/editar.html', {'producto': producto, 'proveedores': proveedores})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'Productos/eliminar.html', {'producto': producto})