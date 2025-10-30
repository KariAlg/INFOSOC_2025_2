from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from .models import ZonaEstacionamiento, RegistroVehiculo
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, JsonResponse
from django.db.models import Prefetch



#Listas:
def landing_page(request):  
    '''
    Página de inicio. Permite elegir qué zona de estacionamiento visualizar.
    '''
    zonas = ZonaEstacionamiento.objects.all()
    context = {
        "zonas": zonas
    }
    return render(request, "estacionamientos/landing_page.html", context)


def visualizador_estacionamientos(request, zona_id):  
    '''
    Muestra la cantidad de estacionamientos disponibles en la zona indicada por ID.
    '''
    zona = get_object_or_404(ZonaEstacionamiento, id=zona_id)
    context = {"zona": zona}
    return render(request, "estacionamientos/visualizador.html", context)

def estado_zona(request, zona_id):
    """
    Devuelve el estado actual de una zona en formato JSON.
    """
    try:
        zona = ZonaEstacionamiento.objects.get(id=zona_id)
        data = {
            "nombre_zona": zona.nombre_zona,
            "disponibles": zona.disponibles,
            "totales": zona.n_estacionamientos_totales,
        }
        return JsonResponse(data)
    except ZonaEstacionamiento.DoesNotExist:
        return JsonResponse({"error": "Zona no encontrada"}, status=404)


@login_required
def crear_estacionamientos(request):
    """
    Permite crear una nueva zona de estacionamiento.
    El número de disponibles se inicializa igual a n_estacionamientos_totales.
    """
    if request.user.cargo == "GUARDIA":
        raise Http404("Página no encontrada")
    if request.method == 'POST':
        nombre_zona = request.POST.get('nombre_zona')
        n_totales = request.POST.get('n_estacionamientos_totales')

        if not nombre_zona or not n_totales:
            return render(request, 'estacionamientos/crear_estacionamientos.html', {
                'error': 'Debes ingresar todos los campos.'
            })

        try:
            n_totales = int(n_totales)
            if n_totales <= 0:
                raise ValueError("El número de estacionamientos debe ser positivo.")

            # Creamos la zona con disponibles = totales
            nueva_zona = ZonaEstacionamiento.objects.create(
                nombre_zona=nombre_zona,
                n_estacionamientos_totales=n_totales,
                disponibles=n_totales
            )
            return redirect('modificar_estacionamientos')

        except IntegrityError:
            return render(request, 'estacionamientos/crear_estacionamientos.html', {
                'error': 'Ya existe una zona con ese nombre.'
            })
        except ValueError as e:
            return render(request, 'estacionamientos/crear_estacionamientos.html', {
                'error': str(e)
            })

    return render(request, 'estacionamientos/crear_estacionamientos.html')

@login_required
def modificar_estacionamientos(request):
    if request.user.cargo == "GUARDIA":
        raise Http404("Página no encontrada")
    zonas = ZonaEstacionamiento.objects.all()
    zona_id = request.GET.get('zona') or request.POST.get('zona')
    zona = None

    if zona_id:
        zona = get_object_or_404(ZonaEstacionamiento, id=zona_id)

    # --- Guardar modificaciones ---
    if request.method == 'POST' and 'guardar' in request.POST and zona:
        nuevo_nombre = request.POST.get('nombre_zona')
        nuevos_totales = int(request.POST.get('n_estacionamientos_totales'))

        # Validación: no permitir reducir totales por debajo de los ocupados
        ocupados = zona.n_estacionamientos_totales - zona.disponibles
        if nuevos_totales < ocupados:
            return render(request, "estacionamientos/modificar_estacionamientos.html", {
                "zonas": zonas,
                "zona_seleccionada": zona,
                "error": f"No puedes establecer menos de {ocupados} estacionamientos: ya están ocupados.",
            })

        # Actualizar zona
        try:
            zona.nombre_zona = nuevo_nombre
            zona.n_estacionamientos_totales = nuevos_totales
            zona.disponibles = max(0, nuevos_totales - ocupados)
            zona.save()
            return redirect('modificar_estacionamientos')

        except IntegrityError:
            return render(request, "estacionamientos/modificar_estacionamientos.html", {
                "zonas": zonas,
                "zona_seleccionada": zona,
                "error": "Ya existe una zona con ese nombre. Usa un nombre distinto."
            })

    # --- Eliminar zona ---
    if request.method == 'POST' and 'eliminar' in request.POST and zona:
        try:
            zona.delete_estacionamiento()
            return redirect('modificar_estacionamientos')
        except ValidationError as e:
            return render(request, "estacionamientos/modificar_estacionamientos.html", {
                "zonas": zonas,
                "zona_seleccionada": zona,
                "error": e.message
            })

    context = {
        "zonas": zonas,
        "zona_seleccionada": zona
    }
    return render(request, "estacionamientos/modificar_estacionamientos.html", context)

@login_required
def registrar_entrada(request):
    zonas = ZonaEstacionamiento.objects.all()
    zona_id = request.GET.get('zona') or request.POST.get('zona')
    zona = None

    if zona_id:
        zona = get_object_or_404(ZonaEstacionamiento, id=zona_id)

    if request.method == 'POST' and zona:
        patente = request.POST.get('patente')
        nombre = request.POST.get('nombre_conductor')
        apellido = request.POST.get('apellido_conductor')
        rut = request.POST.get('rut_conductor')

        # Usa el método del modelo en lugar de hacerlo manualmente
        nuevo_registro = RegistroVehiculo.ingresar(
            patente=patente,
            nombre=nombre,
            apellido=apellido,
            rut=rut,
            zona=zona
        )

        if nuevo_registro:
            return redirect('panel_home')
        else:
            return render(request, "estacionamientos/registrar_entrada.html", {
                "zonas": zonas,
                "zona_seleccionada": zona,
                "error": "No se pudo registrar la entrada. Verifica los datos o la disponibilidad."
            })

    return render(request, "estacionamientos/registrar_entrada.html", {
        "zonas": zonas,
        "zona_seleccionada": zona
    })

@login_required
def registrar_salida(request):
    """
    Registra la salida de un vehículo:
    1. Elige zona de estacionamiento.
    2. Muestra los vehículos estacionados sin hora de salida.
    3. Marca la salida del vehículo seleccionado.
    """
    zonas = ZonaEstacionamiento.objects.all()
    zona_id = request.GET.get('zona') or request.POST.get('zona')
    zona = None

    if zona_id:
        zona = get_object_or_404(ZonaEstacionamiento, id=zona_id)
        # Filtramos los vehículos actualmente estacionados (sin hora_salida)
        vehiculos = RegistroVehiculo.objects.filter(
            zona_estacionamiento=zona,
            hora_salida__isnull=True
        )
    else:
        vehiculos = None

    if request.method == 'POST' and zona:
        patente = request.POST.get('patente')
        registro = RegistroVehiculo.salida(patente)

        if registro:
            return redirect('panel_home')
        else:
            return render(request, "estacionamientos/registrar_salida.html", {
                "zonas": zonas,
                "zona_seleccionada": zona,
                "vehiculos": vehiculos,
                "error": "No se pudo registrar la salida. Verifique la patente."
            })

    return render(request, "estacionamientos/registrar_salida.html", {
        "zonas": zonas,
        "zona_seleccionada": zona,
        "vehiculos": vehiculos
    })


#pendientes:
@login_required
def dashboard_autos_estacionados(request):
    '''
    Muestra los vehículos actualmente estacionados, separados por zona y tiempo dentro.
    Desde aquí se puede marcar la salida de un auto.
    '''
    zonas_con_vehiculos = ZonaEstacionamiento.objects.prefetch_related('registros')
    return render(request, "estacionamientos/dashboard_autos_estacionados.html",{
        "vehiculos": zonas_con_vehiculos,
    })

@login_required
def visualizacion_datos(request):
    '''
    Vista de consultas sobre la base de datos:
    - Ver entradas/salidas de un día (op1)
    - Historial de un vehículo por patente (op2)
    - Filtrar registros por zona y fecha (op3)
    '''
    if request.method == 'GET':
        verES = request.GET.get('op1')
        historialVehiculo = request.GET.get('op2')
        filtrarRegistros = request.GET.get('op3')

        if verES:
            diaAConsultar = request.GET.get('dia')
            registro_del_dia = RegistroVehiculo.objects.filter(hora_entrada__date=diaAConsultar)
            registro_del_dia = Prefetch('registros',queryset=registro_del_dia)
            registro_del_dia = ZonaEstacionamiento.objects.prefetch_related(registro_del_dia)
            if diaAConsultar:
                return render(request, "estacionamientos/visualizacion_datos.html",{
                    "opcionSeleccionada": 1,
                    "registros": registro_del_dia
                })
            return render(request, "estacionamientos/visualizacion_datos.html",{
                "opcionSeleccionada": 1
            })
        elif historialVehiculo:
            patenteAConsultar = request.GET.get('patente')
            registro_patente = RegistroVehiculo.objects.filter(patente=patenteAConsultar)
            if patenteAConsultar:
                return render(request, "estacionamientos/visualizacion_datos.html",{
                    "opcionSeleccionada": 2,
                    "registros": registro_patente,
                    "patenteConsultada": patenteAConsultar
                })
            return render(request, "estacionamientos/visualizacion_datos.html",{
                "opcionSeleccionada": 2
            })
        elif filtrarRegistros:
            zonas = ZonaEstacionamiento.objects.all()
            diaAConsultar = request.GET.get('dia')
            zonaAConsultar =  request.GET.get('zona')
            registro_zona = RegistroVehiculo.objects.filter(hora_entrada__date=diaAConsultar, zona_estacionamiento=zonaAConsultar)
            if diaAConsultar and zonaAConsultar:
                zonaStr = get_object_or_404(ZonaEstacionamiento, id=zonaAConsultar)
                return render(request, "estacionamientos/visualizacion_datos.html",{
                    "opcionSeleccionada": 3,
                    "registros": registro_zona,
                    "zona": zonaStr,
                    "dia": diaAConsultar
                })
            return render(request, "estacionamientos/visualizacion_datos.html",{
                "opcionSeleccionada": 3,
                "zonas": zonas
            })
        else:
            return render(request, "estacionamientos/visualizacion_datos.html")

@login_required
def descargar_reporte(request):
    '''
    Genera y descarga un reporte en Excel filtrado por:
    - Rango de fechas
    - Zona de estacionamiento
    - Otros criterios de búsqueda
    '''
    context = {}
    return render(request, "estacionamientos/descargar_reporte.html", context)