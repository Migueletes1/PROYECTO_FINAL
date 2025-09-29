from django.contrib.auth.models import AbstractUser
from django.db import models



class Usuario(AbstractUser):
    ADMIN = "ADMIN"
    EMPRESA = "EMPRESA"
    APRENDIZ = "APRENDIZ"
    INSTRUCTOR = "INSTRUCTOR"

    ROLES = [
        (ADMIN, "Administrador"),
        (EMPRESA, "Empresa"),
        (APRENDIZ, "Aprendiz"),
        (INSTRUCTOR, "Instructor"),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, default=APRENDIZ)

    def __str__(self):
        return f"{self.username} ({self.rol})"


class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    area = models.CharField(max_length=100)
    duracion_semanas = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=[("EN_DESARROLLO","En desarrollo"),("COMPLETADO","Completado"),("PENDIENTE","Pendiente")], default="PENDIENTE")
    empresa = models.ForeignKey("Usuarios.Usuario", on_delete=models.CASCADE, related_name="proyectos_empresa")
    aprendices = models.ManyToManyField("Usuarios.Usuario", blank=True, related_name="proyectos_asignados")
    creado_en = models.DateTimeField(auto_now_add=True)


