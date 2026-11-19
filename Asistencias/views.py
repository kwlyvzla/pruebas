from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import RegistroAsistencia
from Empleados.models import Empleado


def lista_asistencias(request):
    asistencias = RegistroAsistencia.objects.select_related('empleado').all()
    return render(request, 'Asistencias/lista.html', {'asistencias': asistencias})


def agregar_asistencia(request):
    empleados = Empleado.objects.filter(activo=True).order_by('nombre_completo')

    if request.method == 'POST':
        empleado_id = request.POST.get('empleado')
        fecha = request.POST.get('fecha')
        hora_entrada = request.POST.get('hora_entrada') or None
        hora_salida = request.POST.get('hora_salida') or None
        estado = request.POST.get('estado')
        observaciones = request.POST.get('observaciones') or ''

        empleado = get_object_or_404(Empleado, id=empleado_id)

        RegistroAsistencia.objects.create(
            empleado=empleado,
            fecha=fecha,
            hora_entrada=hora_entrada,
            hora_salida=hora_salida,
            estado=estado,
            observaciones=observaciones,
        )
        return redirect('lista_asistencias')

    return render(request, 'Asistencias/agregar.html', {
        'empleados': empleados,
        'hoy': timezone.now().date(),
    })


def editar_asistencia(request, id):
    asistencia = get_object_or_404(RegistroAsistencia, id=id)
    empleados = Empleado.objects.filter(activo=True).order_by('nombre_completo')

    if request.method == 'POST':
        asistencia.empleado_id = request.POST.get('empleado')
        asistencia.fecha = request.POST.get('fecha')
        asistencia.hora_entrada = request.POST.get('hora_entrada') or None
        asistencia.hora_salida = request.POST.get('hora_salida') or None
        asistencia.estado = request.POST.get('estado')
        asistencia.observaciones = request.POST.get('observaciones') or ''
        asistencia.save()
        return redirect('lista_asistencias')

    return render(request, 'Asistencias/editar.html', {
        'asistencia': asistencia,
        'empleados': empleados,
    })


def eliminar_asistencia(request, id):
    asistencia = get_object_or_404(RegistroAsistencia, id=id)

    if request.method == 'POST':
        asistencia.delete()
        return redirect('lista_asistencias')

    return render(request, 'Asistencias/eliminar.html', {'asistencia': asistencia})
