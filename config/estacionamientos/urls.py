from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("zona/<int:zona_id>/", views.visualizador_estacionamientos, name="visualizador_estacionamientos"),
    path("crear/", views.crear_estacionamientos, name="crear_estacionamientos"),
    path("modificar/<int:zona_id>/", views.modificar_estacionamientos, name="modificar_estacionamientos"),

    path("entrada/", views.registrar_entrada, name="registrar_entrada"),
    path("salida/", views.registrar_salida, name="registrar_salida"),
    path("dashboard/", views.dashboard_autos_estacionados, name="dashboard_autos_estacionados"),

    path("reporte/", views.descargar_reporte, name="descargar_reporte"),
    path("visualizacion/", views.visualizacion_datos, name="visualizacion_datos"),
]