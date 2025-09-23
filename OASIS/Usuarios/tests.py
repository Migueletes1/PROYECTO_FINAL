from django.test import TestCase
from django.urls import reverse
from .models import Usuario

class AuthTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username="testuser", password="12345", rol=Usuario.APRENDIZ  # ✅ CORREGIDO
        )

    def test_login_correcto(self):
        login = self.client.login(username="testuser", password="12345")
        self.assertTrue(login)

    def test_login_incorrecto(self):
        login = self.client.login(username="testuser", password="wrong")
        self.assertFalse(login)

    def test_registro(self):
        response = self.client.post(reverse("registro"), {
            "username": "nuevo",
            "password1": "passPrueba123",
            "password2": "passPrueba123",
            "rol": Usuario.EMPRESA,
            "email": "test@example.com",  # ✅ AGREGAR email requerido
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Usuario.objects.filter(username="nuevo").exists())
