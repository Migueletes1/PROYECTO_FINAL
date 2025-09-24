from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import RegistroForm, LoginForm
from .models import Usuario
from .decorators import role_required

# Agregar estas nuevas vistas a tu views.py existente

@login_required
@role_required(['APRENDIZ'])
def dashboard_aprendiz(request):
    """Dashboard específico para aprendices"""
    # Aquí puedes agregar lógica para obtener datos específicos del estudiante
    materias_activas = 6  # Ejemplo estático
    promedio_general = 4.2
    tareas_pendientes = 12
    asistencia = 85
    
    return render(request, 'usuarios/dashboard_aprendiz.html', {
        'materias_activas': materias_activas,
        'promedio_general': promedio_general,
        'tareas_pendientes': tareas_pendientes,
        'asistencia': asistencia,
    })

# Actualizar la vista home para redirigir correctamente
def home(request):
    if request.user.is_authenticated:
        # Redirigir según el rol del usuario autenticado
        if request.user.rol == Usuario.ADMIN:
            return redirect('admin_dashboard')
        elif request.user.rol == Usuario.EMPRESA:
            return redirect('empresa_dashboard')
        elif request.user.rol == Usuario.INSTRUCTOR:
            return redirect('instructor_dashboard')
        else:  # APRENDIZ
            return redirect('dashboard_aprendiz')
    return render(request, 'usuarios/index.html')



def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.username} creado exitosamente!')
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.username}!')
                
                # Redirigir según el rol
                if user.rol == Usuario.ADMIN:
                    return redirect('admin_dashboard')
                elif user.rol == Usuario.EMPRESA:
                    return redirect('empresa_dashboard')
                elif user.rol == Usuario.INSTRUCTOR:
                    return redirect('instructor_dashboard')
                else:
                    return redirect('inicio')
            else:
                messages.error(request, 'Credenciales inválidas.')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = LoginForm()
    return render(request, "usuarios/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

# DASHBOARDS POR ROL
@login_required
@role_required(['ADMIN'])
def admin_dashboard(request):
    total_usuarios = Usuario.objects.count()
    usuarios_por_rol = {
        'admins': Usuario.objects.filter(rol=Usuario.ADMIN).count(),
        'empresas': Usuario.objects.filter(rol=Usuario.EMPRESA).count(),
        'instructores': Usuario.objects.filter(rol=Usuario.INSTRUCTOR).count(),
        'aprendices': Usuario.objects.filter(rol=Usuario.APRENDIZ).count(),
    }
    
    return render(request, "usuarios/admin_dashboard.html", {
        'total_usuarios': total_usuarios,
        'usuarios_por_rol': usuarios_por_rol,
    })

@login_required
@role_required(['EMPRESA'])
def empresa_dashboard(request):
    return render(request, "usuarios/empresa_dashboard.html")

@login_required
@role_required(['INSTRUCTOR'])
def instructor_dashboard(request):
    return render(request, "usuarios/instructor_dashboard.html")

# GESTIÓN DE USUARIOS (Solo para ADMIN)
@login_required
@role_required(['ADMIN'])
def listar_usuarios(request):
    usuarios_list = Usuario.objects.all().order_by('-date_joined')
    
    # Filtros
    rol_filtro = request.GET.get('rol')
    buscar = request.GET.get('buscar')
    
    if rol_filtro:
        usuarios_list = usuarios_list.filter(rol=rol_filtro)
    
    if buscar:
        usuarios_list = usuarios_list.filter(username__icontains=buscar)
    
    # Paginación
    paginator = Paginator(usuarios_list, 10)  # 10 usuarios por página
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)
    
    return render(request, 'usuarios/listar_usuarios.html', {
        'usuarios': usuarios,
        'roles': Usuario.ROLES,
        'rol_actual': rol_filtro,
        'buscar_actual': buscar or '',
    })

@login_required
@role_required(['ADMIN'])
def editar_usuario(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('listar_usuarios')
    
    if request.method == 'POST':
        # Actualizar datos básicos
        usuario.username = request.POST.get('username', usuario.username)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.rol = request.POST.get('rol', usuario.rol)
        usuario.is_active = request.POST.get('is_active') == 'on'
        
        try:
            usuario.save()
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente.')
            return redirect('listar_usuarios')
        except Exception as e:
            messages.error(request, f'Error al actualizar usuario: {str(e)}')
    
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})

@login_required
@role_required(['ADMIN'])
def eliminar_usuario(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
        if usuario == request.user:
            messages.error(request, 'No puedes eliminarte a ti mismo.')
        else:
            username = usuario.username
            usuario.delete()
            messages.success(request, f'Usuario {username} eliminado exitosamente.')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
    
    return redirect('listar_usuarios')

@login_required
def perfil_usuario(request):
    if request.method == 'POST':
        # Actualizar perfil del usuario actual
        request.user.email = request.POST.get('email', request.user.email)
        
        # Cambiar contraseña si se proporciona
        nueva_password = request.POST.get('nueva_password')
        if nueva_password:
            password_actual = request.POST.get('password_actual')
            if request.user.check_password(password_actual):
                request.user.set_password(nueva_password)
                messages.success(request, 'Contraseña actualizada. Por favor, inicia sesión nuevamente.')
                logout(request)
                return redirect('login')
            else:
                messages.error(request, 'La contraseña actual es incorrecta.')
                return render(request, 'usuarios/perfil.html')
        
        try:
            request.user.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar perfil: {str(e)}')
    
    return render(request, 'usuarios/perfil.html')
    