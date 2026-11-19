# ProyectoPFD — instrucciones para agentes

Proyecto Django 6.0.7 (Python 3.14.6) de gestión empresarial. Sin README previo. Base de datos por defecto: **SQLite** (`db.sqlite3`, ya creada con migraciones aplicadas).

## Comandos clave (ejecutar desde la raíz del proyecto)
- Instalar dependencias: `pip install -r requirements.txt`
- Levantar servidor: `python manage.py runserver` → `http://127.0.0.1:8000/`
- Migraciones: `python manage.py makemigrations <app>` y `python manage.py migrate`
- Crear superusuario para `/admin/`: `python manage.py createsuperuser`
- Tests (stubs de Django en cada `tests.py`): `python manage.py test`

## Estructura y convenciones
- Apps instaladas: `Proveedores`, `Productos`, `Clientes`, `Empleados`, `Bascula`, `ChatBot`, `Asistencias`.
- Cada app tiene: `models.py`, `views.py`, `urls.py`, `admin.py`, `templates/<App>/`.
- URLs raíz en `ProyectoPFD/urls.py`: cada app montada en su plural (`/productos/`, `/asistencias/`, etc.). Root `/` renderiza `templates/index.html`.
- Templates extienden `base.html` y abren `{% block contenido %}`; **deben cerrar siempre con `{% endblock %}`** (error frecuente: tag sin cerrar → `TemplateSyntaxError`).
- `templates/base.html` y `templates/index.html` están en `templates/` (cargadas vía `TEMPLATES DIRS`), no dentro de una app.

## Gotchas verificados (no adivinar)
- `Productos/apps.py`: la clase debe ser `ProductosConfig` con `name = 'Productos'`. Carpeta, `INSTALLED_APPS` y `AppConfig.name` deben coincidir exactamente (antes estaba mal escrito como `Prodcutos`).
- `ChatBot/serializers.py`: el archivo se llama `serializers.py` (con la 'i'), no `seralizers.py`.
- Base de datos: `settings.py` usa SQLite. El bloque SQL Server (mssql/ODBC Driver 18, `localhost:1433`) está **comentado**. No requiere SQL Server para correr localmente. Python 3.14 es muy nuevo; algunos paquetes de SQL Server pueden carecer de wheels.
- No existe carpeta `static/`; `STATICFILES_DIRS` la incluye solo si existe.

## Arquitectura de bajo nivel
- `Producto` referencia a `Proveedor` (`ForeignKey`, `SET_NULL`).
- `RegistroAsistencia` (app `Asistencias`) referencia a `Empleado` con `unique_together = ['empleado', 'fecha']`.
- ChatBot usa `rest_framework` con serializador `MensajeChatSerializer` y vistas `@api_view`.
- Bascula incluye `usb_connector.py` con `BasculaSimulador` (genera pesos aleatorios y guarda `RegistroPeso`); no requiere hardware real.

## Qué NO hacer
- No cambiar `ENGINE` a `mssql` sin tener SQL Server corriendo y los controladores ODBC instalados.
- No crear apps sin agregar su nombre a `INSTALLED_APPS` y montar su `urls.py` en `ProyectoPFD/urls.py`.
