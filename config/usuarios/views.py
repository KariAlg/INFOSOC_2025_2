from django.shortcuts import render

# Create your views here.
def login_view(request):
    '''
    Página de inicio de sesión para usuarios.
    '''
    context = {}
    return render(request, "usuarios/login.html", context)


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
