from django.shortcuts import render

# Create your views here.

def landing_page(request):
    '''
    Página de inicio. Permite elegir qué zona de estacionamiento visualizar.
    '''
    context = {}
    return render(request, "estacionamientos/landing_page.html", context)


def visualizador_estacionamientos(request, zona_id):
    '''
    Muestra la cantidad de estacionamientos disponibles en la zona indicada por ID.
    '''
    context = {"zona_id": zona_id}
    return render(request, "estacionamientos/visualizador.html", context)


def crear_estacionamientos(request):
    '''
    Formulario para crear una nueva zona de estacionamientos.
    '''
    context = {}
    return render(request, "estacionamientos/crear_estacionamientos.html", context)


def modificar_estacionamientos(request, zona_id):
    '''
    Permite modificar una zona existente o eliminarla.
    '''
    context = {"zona_id": zona_id}
    return render(request, "estacionamientos/modificar_estacionamientos.html", context)


def registrar_entrada(request):
    '''
    Registra la entrada de un vehículo:
    - Elige zona de estacionamiento.
    - Rellena datos de patente, conductor, etc.
    '''
    context = {}
    return render(request, "estacionamientos/registrar_entrada.html", context)


def registrar_salida(request):
    '''
    Registra la salida de un vehículo:
    - Se busca por patente o selecciona desde el dashboard de autos estacionados.
    '''
    context = {}
    return render(request, "estacionamientos/registrar_salida.html", context)


def dashboard_autos_estacionados(request):
    '''
    Muestra los vehículos actualmente estacionados, separados por zona y tiempo dentro.
    Desde aquí se puede marcar la salida de un auto.
    '''
    context = {}
    return render(request, "estacionamientos/dashboard_autos.html", context)


def descargar_reporte(request):
    '''
    Genera y descarga un reporte en Excel filtrado por:
    - Rango de fechas
    - Zona de estacionamiento
    - Otros criterios de búsqueda
    '''
    context = {}
    return render(request, "estacionamientos/descargar_reporte.html", context)


def visualizacion_datos(request):
    '''
    Vista de consultas sobre la base de datos:
    - Ver entradas/salidas de un día
    - Historial de un vehículo por patente
    - Filtrar registros por zona y fecha
    '''
    context = {}
    return render(request, "estacionamientos/visualizacion_datos.html", context)