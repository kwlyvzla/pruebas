from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado

def lista_empleados(request):
    """Mostrar todos los empleados"""
    empleados = Empleado.objects.filter(activo=True).order_by('numero_empleado')
    return render(request, 'Empleados/lista.html', {'empleados': empleados})

def agregar_empleado(request):
    """Agregar un nuevo empleado"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        puesto = request.POST.get('puesto')
        departamento = request.POST.get('departamento')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        salario = request.POST.get('salario')
        activo = request.POST.get('activo') == 'on'
        
        if nombre:
            Empleado.objects.create(
                nombre=nombre,
                email=email or '',
                telefono=telefono or '',
                direccion=direccion or '',
                puesto=puesto or '',
                departamento=departamento or '',
                fecha_ingreso=fecha_ingreso or None,
                salario=salario or None,
                activo=activo
            )
            return redirect('lista_empleados')
    
    return render(request, 'Empleados/agregar.html')

def editar_empleado(request, id):
    """Editar un empleado existente"""
    empleado = get_object_or_404(Empleado, id=id)
    
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.email = request.POST.get('email')
        empleado.telefono = request.POST.get('telefono')
        empleado.direccion = request.POST.get('direccion')
        empleado.puesto = request.POST.get('puesto')
        empleado.departamento = request.POST.get('departamento')
        empleado.fecha_ingreso = request.POST.get('fecha_ingreso') or None
        empleado.salario = request.POST.get('salario') or None
        empleado.activo = request.POST.get('activo') == 'on'
        empleado.save()
        return redirect('lista_empleados')
    
    return render(request, 'Empleados/editar.html', {'empleado': empleado})

def eliminar_empleado(request, id):
    """Eliminar un empleado (con confirmación)"""
    empleado = get_object_or_404(Empleado, id=id)
    
    if request.method == 'POST':
        empleado.delete()
        return redirect('lista_empleados')
    
    return render(request, 'Empleados/eliminar.html', {'empleado': empleado})