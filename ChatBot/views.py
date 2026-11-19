from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

# --- Modelos ---
from .models import MensajeChat
from Asistencias.models import RegistroAsistencia
from Empleados.models import Empleado

# --- Serializadores ---
from .serializers import MensajeChatSerializer, RegistroAsistenciaSerializer


# ============================================================
# CHAT BOT (funcionalidad original restaurada)
# ============================================================
def chat_view(request):
    empleados = Empleado.objects.filter(activo=True).order_by('nombre_completo')
    return render(request, 'ChatBot/chat.html', {'empleados': empleados})


@csrf_exempt
def seleccionar_empleado(request):
    """Guarda el empleado seleccionado en la sesión del chat."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            empleado_id = data.get('empleado_id')
            if not empleado_id:
                return JsonResponse({'error': 'empleado_id requerido'}, status=400)
            empleado = get_object_or_404(Empleado, id=empleado_id, activo=True)
            request.session['chat_empleado_id'] = empleado.id
            request.session['chat_empleado_nombre'] = empleado.nombre_completo
            return JsonResponse({
                'status': 'ok',
                'empleado': f"{empleado.numero_empleado} - {empleado.nombre_completo}"
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def limpiar_sesion_chat(request):
    """Limpia la selección de empleado de la sesión para permitir cambiar."""
    if request.method == 'POST':
        request.session.pop('chat_empleado_id', None)
        request.session.pop('chat_empleado_nombre', None)
        return JsonResponse({'status': 'ok', 'mensaje': 'Sesión limpiada. Puedes seleccionar otro empleado.'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@api_view(['POST'])
def guardar_mensaje(request):
    serializer = MensajeChatSerializer(data=request.data)
    if serializer.is_valid():
        mensaje = serializer.save()
        return Response({
            'status': 'ok',
            'id_mensaje': mensaje.id_mensaje,
            'fecha_envio': mensaje.fecha_envio,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def procesar_mensaje(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje_usuario = data.get('mensaje', '').strip().upper()
            ubicacion = data.get('ubicacion', 'No especificada')

            # Obtener el empleado de la sesión
            empleado_id = request.session.get('chat_empleado_id')
            empleado_nombre = request.session.get('chat_empleado_nombre', 'Empleado')

            if not empleado_id:
                return JsonResponse({
                    'respuesta': ("⚠️ Primero debes seleccionar tu empleado.\n"
                                  "Usa el selector de arriba o escribe tu número de empleado.")
                }, status=400)

            empleado = get_object_or_404(Empleado, id=empleado_id)
            hoy = timezone.now().date()
            ahora = timezone.now().time()

            if mensaje_usuario in ['', 'HOLA', 'INICIO', 'MENU']:
                respuesta = (f"👋 ¡Hola {empleado.nombre_completo}!\n"
                             "Por favor, selecciona una opción:\n"
                             "1️⃣ Entrada\n2️⃣ Salida")
                MensajeChat.objects.create(
                    tipo='MENU', contenido=respuesta, remitente='Bot',
                    ubicacion=ubicacion
                )
                return JsonResponse({'respuesta': respuesta})

            if mensaje_usuario in ['1', 'ENTRADA']:
                # Evitar duplicado mismo día
                ya_existe = RegistroAsistencia.objects.filter(
                    empleado=empleado, fecha=hoy
                ).exists()
                if ya_existe:
                    respuesta = (f"⚠️ Ya tienes una entrada registrada hoy ({hoy.strftime('%d/%m/%Y')}).")
                else:
                    RegistroAsistencia.objects.create(
                        empleado=empleado,
                        fecha=hoy,
                        hora_entrada=ahora,
                        estado='PRESENTE',
                        observaciones='Registrado vía ChatBot'
                    )
                    msg = MensajeChat.objects.create(
                        tipo='ENTRADA',
                        contenido=f"El usuario {empleado.nombre_completo} ({empleado.numero_empleado}) registró una ENTRADA",
                        remitente=empleado.nombre_completo,
                        ubicacion=ubicacion,
                    )
                    respuesta = (f"✅ **Entrada registrada** para {empleado.nombre_completo}.\n"
                                 f"🕐 Hora: {ahora.strftime('%H:%M:%S')}\n"
                                 f"📍 Ubicación: {ubicacion}")
                return JsonResponse({'respuesta': respuesta})

            if mensaje_usuario in ['2', 'SALIDA']:
                registro = RegistroAsistencia.objects.filter(
                    empleado=empleado, fecha=hoy
                ).first()
                if not registro:
                    respuesta = ("⚠️ No tienes una entrada registrada hoy. "
                                 "Registra primero tu entrada.")
                elif registro.hora_salida:
                    respuesta = (f"⚠️ Ya registraste tu salida hoy ({hoy.strftime('%d/%m/%Y')}).")
                else:
                    registro.hora_salida = ahora
                    registro.save()
                    msg = MensajeChat.objects.create(
                        tipo='SALIDA',
                        contenido=f"El usuario {empleado.nombre_completo} ({empleado.numero_empleado}) registró una SALIDA",
                        remitente=empleado.nombre_completo,
                        ubicacion=ubicacion,
                    )
                    respuesta = (f"✅ **Salida registrada** para {empleado.nombre_completo}.\n"
                                 f"🕐 Hora: {ahora.strftime('%H:%M:%S')}\n"
                                 f"📍 Ubicación: {ubicacion}")
                return JsonResponse({'respuesta': respuesta})

            respuesta = ("❌ Opción no válida. Escribe **1** para Entrada o **2** para Salida.")
            return JsonResponse({'respuesta': respuesta})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def recibir_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tipo = data.get('tipo', 'ENTRADA')
            contenido = data.get('contenido', 'Mensaje desde webhook')
            remitente = data.get('remitente', 'Webhook')
            ubicacion = data.get('ubicacion', '')
            mensaje = MensajeChat.objects.create(
                tipo=tipo, contenido=contenido, remitente=remitente, ubicacion=ubicacion
            )
            return JsonResponse({'status': 'ok', 'id_mensaje': mensaje.id_mensaje}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


# ============================================================
# REGISTRO DE ASISTENCIA (vistas agregadas)
# ============================================================
def lista_asistencias(request):
    asistencias = RegistroAsistencia.objects.select_related('empleado').all()
    return render(request, 'ChatBot/lista_asistencias.html', {'asistencias': asistencias})


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
        return redirect('chat_asistencias')

    return render(request, 'ChatBot/agregar_asistencia.html', {
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
        return redirect('chat_asistencias')

    return render(request, 'ChatBot/editar_asistencia.html', {
        'asistencia': asistencia,
        'empleados': empleados,
    })


def eliminar_asistencia(request, id):
    asistencia = get_object_or_404(RegistroAsistencia, id=id)

    if request.method == 'POST':
        asistencia.delete()
        return redirect('chat_asistencias')

    return render(request, 'ChatBot/eliminar_asistencia.html', {'asistencia': asistencia})


# ============================================================
# KIOSCO DE CHECADA (entrada/salida rápida tipo pantalla táctil)
# ============================================================
def kiosco_view(request):
    """Pantalla principal del kiosco con lista de empleados y su estado de hoy."""
    empleados = Empleado.objects.filter(activo=True).order_by('nombre_completo')
    hoy = timezone.now().date()

    # Estado de checada de cada empleado hoy
    estado_empleados = []
    for emp in empleados:
        registro = RegistroAsistencia.objects.filter(empleado=emp, fecha=hoy).first()
        # Formatear horas en la vista para evitar problemas con filtros |time en templates
        hora_entrada_str = registro.hora_entrada.strftime('%H:%M') if registro and registro.hora_entrada else ''
        hora_salida_str = registro.hora_salida.strftime('%H:%M') if registro and registro.hora_salida else ''

        # Determinar estado para el template (evitar lógica compleja en Django templates)
        if not registro:
            estado = 'sin_registro'
        elif registro.hora_entrada and not registro.hora_salida:
            estado = 'entrada_solo'
        elif registro.hora_entrada and registro.hora_salida:
            estado = 'completo'
        else:
            estado = 'sin_registro'

        estado_empleados.append({
            'empleado': emp,
            'registro': registro,
            'estado': estado,
            'hora_entrada_str': hora_entrada_str,
            'hora_salida_str': hora_salida_str,
        })

    return render(request, 'ChatBot/kiosco.html', {
        'estado_empleados': estado_empleados,
        'hoy': hoy,
    })


@csrf_exempt
def kiosco_checar(request):
    """Endpoint para registrar checada desde el kiosco."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            empleado_id = data.get('empleado_id')
            tipo = data.get('tipo', 'AUTO')  # 'ENTRADA', 'SALIDA' o 'AUTO'

            if not empleado_id:
                return JsonResponse({'error': 'empleado_id requerido'}, status=400)

            empleado = get_object_or_404(Empleado, id=empleado_id, activo=True)
            hoy = timezone.localtime().date()
            ahora = timezone.localtime().time()

            registro = RegistroAsistencia.objects.filter(
                empleado=empleado, fecha=hoy
            ).first()

            if tipo == 'AUTO':
                # Lógica automática: si no hay registro → entrada, si hay entrada sin salida → salida
                if not registro:
                    RegistroAsistencia.objects.create(
                        empleado=empleado,
                        fecha=hoy,
                        hora_entrada=ahora,
                        estado='PRESENTE',
                        observaciones='Registrado vía Kiosco'
                    )
                    return JsonResponse({
                        'status': 'ok',
                        'accion': 'ENTRADA',
                        'mensaje': f'Entrada registrada para {empleado.nombre_completo} a las {ahora.strftime("%H:%M:%S")}',
                        'hora': ahora.strftime('%H:%M:%S'),
                    })
                elif registro.hora_entrada and not registro.hora_salida:
                    registro.hora_salida = ahora
                    registro.save()
                    return JsonResponse({
                        'status': 'ok',
                        'accion': 'SALIDA',
                        'mensaje': f'Salida registrada para {empleado.nombre_completo} a las {ahora.strftime("%H:%M:%S")}',
                        'hora': ahora.strftime('%H:%M:%S'),
                    })
                else:
                    return JsonResponse({
                        'status': 'info',
                        'accion': 'NINGUNA',
                        'mensaje': f'{empleado.nombre_completo} ya tiene entrada y salida registradas hoy.',
                    })

            elif tipo == 'ENTRADA':
                if registro and registro.hora_entrada:
                    return JsonResponse({
                        'status': 'info',
                        'accion': 'DUPLICADO',
                        'mensaje': f'Ya existe una entrada registrada hoy para {empleado.nombre_completo}.',
                    })
                if not registro:
                    RegistroAsistencia.objects.create(
                        empleado=empleado,
                        fecha=hoy,
                        hora_entrada=ahora,
                        estado='PRESENTE',
                        observaciones='Registrado vía Kiosco'
                    )
                else:
                    registro.hora_entrada = ahora
                    registro.save()
                return JsonResponse({
                    'status': 'ok',
                    'accion': 'ENTRADA',
                    'mensaje': f'Entrada registrada para {empleado.nombre_completo} a las {ahora.strftime("%H:%M:%S")}',
                    'hora': ahora.strftime('%H:%M:%S'),
                })

            elif tipo == 'SALIDA':
                if not registro or not registro.hora_entrada:
                    return JsonResponse({
                        'status': 'error',
                        'accion': 'SIN_ENTRADA',
                        'mensaje': f'{empleado.nombre_completo} no tiene entrada registrada hoy.',
                    }, status=400)
                if registro.hora_salida:
                    return JsonResponse({
                        'status': 'info',
                        'accion': 'DUPLICADO',
                        'mensaje': f'Ya existe una salida registrada hoy para {empleado.nombre_completo}.',
                    })
                registro.hora_salida = ahora
                registro.save()
                return JsonResponse({
                    'status': 'ok',
                    'accion': 'SALIDA',
                    'mensaje': f'Salida registrada para {empleado.nombre_completo} a las {ahora.strftime("%H:%M:%S")}',
                    'hora': ahora.strftime('%H:%M:%S'),
                })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
