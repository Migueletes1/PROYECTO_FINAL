from django.urls import path
from . import views

urlpatterns = [
    # Add 'inicio' as a name for the home view
    path('', views.home, name='home'),
    path('', views.home, name='inicio'), # You can add a new line like this, but it's redundant.
    # The best practice is to just add it to the existing path.
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('panel/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('empresa/dashboard/', views.empresa_dashboard, name='empresa_dashboard'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('aprendiz/dashboard/', views.dashboard_aprendiz, name='dashboard_aprendiz'),
    path('panel/admin/usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('panel/admin/usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('panel/admin/usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('panel/admin/reportes/', views.reportes, name='reportes'),
    path('panel/admin/usuarios/nuevo/', views.crear_usuario, name='crear_usuario'),
]