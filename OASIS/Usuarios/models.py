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

