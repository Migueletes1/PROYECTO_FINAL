from django.shortcuts import redirect
from django.urls import reverse

class RolRequiredMiddleware:
    """
    Middleware para restringir acceso según rol.
    Usar decoradores o lógica en views junto con este middleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ruta = request.path

        # Ejemplo de restricciones
        if ruta.startswith("/admin-panel/") and (
            not request.user.is_authenticated or request.user.rol != "ADMIN"
        ):
            return redirect(reverse("login"))

        if ruta.startswith("/empresa/") and (
            not request.user.is_authenticated or request.user.rol != "EMPRESA"
        ):
            return redirect(reverse("login"))

        return self.get_response(request)
