from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("home/", views.home_view, name="home"),

    path("crear/", views.crear_usuario, name="crear_usuario"),
    path("modificar/", views.modificar_mi_perfil, name="modificar_mi_perfil"),
    path("borrar/<int:user_id>/", views.borrar_usuario, name="borrar_usuario"),
]