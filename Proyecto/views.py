from django.shortcuts import render
from .models import Tarea

def lista_tareas(request):
    todas_las_tareas = Tarea.objects.all()
    return render(request, 'tareas/lista.html', {
        'tareas': todas_las_tareas
    })