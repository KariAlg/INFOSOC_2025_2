from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.urls import reverse
from utils.utils import normalizar_rut 
from django.contrib import messages
from .forms import UsuarioCreationForm, UsuarioEditForm




#Listas:
def login_view(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        password = request.POST.get('password')

        # 🔹 Normaliza el RUT antes de usarlo
        rut_normalizado = normalizar_rut(rut)

        # 1️⃣ Verifica si existe el usuario
        try:
            user_obj = Usuario.objects.get(rut=rut_normalizado)
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {
                'error_type': 'rut',
                'error_message': 'El RUT ingresado no existe.'
            })

        # 2️⃣ Verifica la contraseña (usa el backend, que también normaliza)
        user = authenticate(request, rut=rut, password=password)
        if user is not None:
            login(request, user)
            return redirect('panel_home')
        else:
            return render(request, 'login.html', {
                'error_type': 'password',
                'error_message': 'La contraseña es incorrecta.'
            })

    return render(request, 'login.html')

@login_required
def panel_home(request):
    usuario = get_object_or_404(Usuario, rut=request.user.rut)
    actions = [
        ["Registrar Entrada", reverse('registrar_entrada')],
        ["Registrar Salida", reverse('registrar_salida')],
        ["Ver vehiculos estacionados (pendiente)", reverse('registrar_salida')],
        ["Consultar registros diarios (pendiente)", reverse('registrar_salida')],
    ]
    if(usuario.cargo != 'GUARDIA'): 
        actions.append( ["Modifcar Zonas de estacionamientos", reverse('modificar_estacionamientos')])
        actions.append( ["Crear Nuevo Usuario", reverse('crear_usuario')])
        actions.append( ["Modificar Usuario Existente", reverse('listar_usuarios')])

    context = {
        "usuario": usuario,
        "actions": actions
    }

    return render(request, 'usuarios/panel_home.html', context)



@login_required
def logout_view(request):
    """
    Cierra la sesión del usuario y redirige a la página de inicio de sesión.
    """
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # usa el name que tengas para tu vista de login

    # Si llega por GET, muestra una página de confirmación opcional
    return render(request, "usuarios/logout.html")




@login_required
def crear_usuario(request):
    usuario = request.user

    # Guardias no pueden crear
    if usuario.es_guardia():
        messages.error(request, "No tienes permiso para crear usuarios.")
        return redirect("panel_home")

    if request.method == "POST":
        form = UsuarioCreationForm(request.POST, usuario=usuario)
        if form.is_valid():
            nuevo_usuario = form.save(commit=False)

            # Si un admin débil intenta crear otro tipo que no sea guardia
            if usuario.es_admin_debil() and nuevo_usuario.cargo != "GUARDIA":
                messages.error(request, "Solo puedes crear Guardias.")
                return redirect("crear_usuario")

            nuevo_usuario.save()
            messages.success(request, f"Usuario '{nuevo_usuario.username}' creado correctamente.")
            return redirect("panel_home")
    else:
        form = UsuarioCreationForm(usuario=usuario)

    return render(request, "usuarios/crear_usuario.html", {"form": form})

@login_required
def listar_usuarios(request):
    usuario = request.user

    # Filtrado según permisos
    if usuario.es_guardia():
        messages.error(request, "No tienes permiso para ver otros usuarios.")
        return redirect("landing_page")
    elif usuario.es_admin_debil():
        usuarios = Usuario.objects.filter(cargo="GUARDIA", is_superuser=False)
    else:  # admin fuerte
        usuarios = Usuario.objects.filter(is_superuser=False)

    return render(request, "usuarios/listar_usuarios.html", {"usuarios": usuarios})


@login_required
def editar_usuario(request, rut):
    usuario_actual = request.user
    usuario_editar = get_object_or_404(Usuario, rut=rut)

    # Restringir acceso según rol
    if usuario_actual.es_guardia():
        messages.error(request, "No tienes permiso para editar usuarios.")
        return redirect("landing_page")
    if usuario_actual.es_admin_debil() and usuario_editar.cargo != "GUARDIA":
        messages.error(request, "Solo puedes editar guardias.")
        return redirect("listar_usuarios")

    if request.method == "POST":
        form = UsuarioEditForm(request.POST, instance=usuario_editar, creador=usuario_actual)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuario {usuario_editar.username} modificado correctamente.")
            return redirect("listar_usuarios")
    else:
        form = UsuarioEditForm(instance=usuario_editar, creador=usuario_actual)

    return render(request, "usuarios/editar_usuario.html", {"form": form, "usuario_obj": usuario_editar})

@login_required
def borrar_usuario(request, rut):
    usuario_actual = request.user
    usuario_obj = get_object_or_404(Usuario, rut=rut)

    # 🔐 Reglas de permisos
    if usuario_actual.es_guardia():
        messages.error(request, "No tienes permiso para eliminar usuarios.")
        return redirect("listar_usuarios")

    if usuario_actual.es_admin_debil() and usuario_obj.cargo != "GUARDIA":
        messages.error(request, "Solo puedes eliminar guardias.")
        return redirect("listar_usuarios")

    # ✅ Confirmación por método POST
    if request.method == "POST":
        nombre = f"{usuario_obj.first_name} {usuario_obj.last_name}"
        usuario_obj.delete()
        messages.success(request, f"Usuario {nombre} eliminado correctamente.")
        return redirect("listar_usuarios")

    # Renderiza confirmación
    return render(request, "usuarios/confirmar_eliminar.html", {"usuario_obj": usuario_obj})


#Pendientes
def modificar_mi_perfil(request):
    '''
    Permite al usuario modificar su propio perfil:
    - Correo, contraseña, nombres
    - No se pueden cambiar RUT ni cargo
    '''
    context = {}
    return render(request, "usuarios/modificar_mi_perfil.html", context)


