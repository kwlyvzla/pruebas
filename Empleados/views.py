from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado
from datetime import datetime

def lista_empleados(request):
    """Mostrar todos los empleados activos"""
    empleados = Empleado.objects.filter(activo=True).order_by('apellidos', 'nombre')
    return render(request, 'Empleados/lista.html', {'empleados': empleados})

def agregar_empleado(request):
    """Agregar un nuevo empleado"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        curp = request.POST.get('curp')
        rfc = request.POST.get('rfc')
        ##email = request.POST.get('email')
        ## telefono = request.POST.get('telefono')
        celular = request.POST.get('celular')
        direccion = request.POST.get('direccion')
        puesto = request.POST.get('puesto')
        fecha_contratacion = request.POST.get('fecha_contratacion')
        salario = request.POST.get('salario')
        nss = request.POST.get('nss')
        numero_empleado = request.POST.get('numero_empleado')
        activo = request.POST.get('activo') == 'on'
        
        # Validar datos obligatorios
        if nombre and apellidos and direccion and numero_empleado and fecha_contratacion:
            Empleado.objects.create(
                nombre=nombre,
                apellidos=apellidos,
                curp=curp or '',
                rfc=rfc or '',
                ##email=email or '',
                ##telefono=telefono or '',
                celular=celular or '',
                direccion=direccion,
                puesto=puesto or 'OTRO',
                fecha_contratacion=fecha_contratacion,
                salario=float(salario) if salario else None,
                nss=nss or '',
                numero_empleado=numero_empleado,
                activo=activo
            )
            return redirect('lista_empleados')
    
    return render(request, 'Empleados/agregar.html')

def editar_empleado(request, id):
    """Editar un empleado existente"""
    empleado = get_object_or_404(Empleado, id=id)
    
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.apellidos = request.POST.get('apellidos')
        empleado.curp = request.POST.get('curp')
        empleado.rfc = request.POST.get('rfc')
        ##empleado.email = request.POST.get('email')
        ##empleado.telefono = request.POST.get('telefono')
        empleado.celular = request.POST.get('celular')
        empleado.direccion = request.POST.get('direccion')
        empleado.puesto = request.POST.get('puesto')
        empleado.fecha_contratacion = request.POST.get('fecha_contratacion')
        empleado.salario = float(request.POST.get('salario')) if request.POST.get('salario') else None
        empleado.nss = request.POST.get('nss')
        empleado.numero_empleado = request.POST.get('numero_empleado')
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