from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from Proveedores.models import Proveedor

# ===== VISTAS PRINCIPALES =====

def lista_productos(request):
    """Mostrar todos los productos"""
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'Productos/lista.html', {'productos': productos})

def agregar_producto(request):
    """Agregar un nuevo producto"""
    proveedores = Proveedor.objects.all().order_by('nombre')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        proveedor_id = request.POST.get('proveedor')
        activo = request.POST.get('activo') == 'on'  # Checkbox
        
        # Validar datos
        if nombre and precio:
            # Buscar el proveedor si existe
            proveedor = None
            if proveedor_id:
                proveedor = get_object_or_404(Proveedor, id=proveedor_id)
            
            # Crear producto
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock or 0,
                proveedor=proveedor,
                activo=activo
            )
            return redirect('lista_productos')
    
    return render(request, 'Productos/agregar.html', {
        'proveedores': proveedores
    })

def editar_producto(request, id):
    """Editar un producto existente"""
    producto = get_object_or_404(Producto, id=id)
    proveedores = Proveedor.objects.all().order_by('nombre')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        proveedor_id = request.POST.get('proveedor')
        activo = request.POST.get('activo') == 'on'
        
        if nombre and precio:
            # Actualizar datos
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.stock = stock or 0
            producto.activo = activo
            
            # Actualizar proveedor
            if proveedor_id:
                producto.proveedor = get_object_or_404(Proveedor, id=proveedor_id)
            else:
                producto.proveedor = None
            
            producto.save()
            return redirect('lista_productos')
    
    return render(request, 'Productos/editar.html', {
        'producto': producto,
        'proveedores': proveedores
    })

def eliminar_producto(request, id):
    """Eliminar un producto (con confirmación)"""
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    
    return render(request, 'Productos/eliminar.html', {'producto': producto})