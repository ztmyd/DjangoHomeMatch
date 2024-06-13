# middleware.py

from django.utils import timezone
from .models import ErrorLog

class Log404ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            # Registrar el error 404 en la base de datos
            ErrorLog.objects.create(
                path=request.path,
                method=request.method,
                timestamp=timezone.now()
            )
        return response
