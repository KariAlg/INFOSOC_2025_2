from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Guardia, AdministrativoDebil, AdministrativoFuerte

# Create your views here.
def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'form': form
            })

@login_required
def home_view(request):
    guard = Guardia.objects.filter(rut=request.user.rut)
    strongAdmin = AdministrativoFuerte.objects.filter(rut=request.user.rut)
    weakAdmin = AdministrativoDebil.objects.filter(rut=request.user.rut)
    rut = request.user.rut
    cargo = request.user.cargo
    return render(request, 'home.html', {
        "rut": rut,
        "cargo": cargo
    })

def logout_view(request):
    '''
    Cierra la sesión del usuario y redirige a la página de inicio.
    '''
    context = {}
    return render(request, "usuarios/logout.html", context)


def crear_usuario(request):
    '''
    Crea una cuenta de usuario para un guardia o administrativo.
    - Recibe correo, nombre, apellido, RUT y cargo.
    - Envía correo con contraseña generada automáticamente.
    '''
    context = {}
    return render(request, "usuarios/crear_usuario.html", context)


def modificar_mi_perfil(request):
    '''
    Permite al usuario modificar su propio perfil:
    - Correo, contraseña, nombres
    - No se pueden cambiar RUT ni cargo
    '''
    context = {}
    return render(request, "usuarios/modificar_mi_perfil.html", context)


def borrar_usuario(request, user_id):
    '''
    Permite eliminar un usuario del sistema.
    - Respeta la jerarquía: solo admin fuerte puede borrar admin débil, etc.
    Primero debe ser capaz de elegir cuál. 
    '''
    context = {"user_id": user_id}
    return render(request, "usuarios/borrar_usuario.html", context)
