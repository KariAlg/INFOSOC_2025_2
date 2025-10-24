from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.panel_home, name="panel_home"),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    

    path("crear/", views.crear_usuario, name="crear_usuario"),
    path("listar/", views.listar_usuarios, name="listar_usuarios"),
    path("editar/<str:rut>/", views.editar_usuario, name="editar_usuario"),

    path("modificar/", views.modificar_mi_perfil, name="modificar_mi_perfil"),
    path("borrar/<str:rut>/", views.borrar_usuario, name="borrar_usuario"),
]