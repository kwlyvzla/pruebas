from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='inicio'),
    path('admin/', admin.site.urls),
    path('proveedores/', include('Proveedores.urls')),
    path('productos/', include('Productos.urls')),
    path('clientes/', include('Clientes.urls')),
    path('empleados/', include('Empleados.urls')),
    path('bascula/', include('Bascula.urls')),
    path('chatbot/', include('ChatBot.urls')),
    path('asistencias/', include('Asistencias.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)