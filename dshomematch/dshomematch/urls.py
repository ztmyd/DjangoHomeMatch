
from django.contrib import admin
from django.urls import path, include
from home_match.views import signup

urlpatterns = [
    path('', signup, name='signup'),  # Define la ruta raíz como la vista signup
    path('admin/', admin.site.urls),  # Ruta de administrador
    path('signup/', include('home_match.urls')),  # Otras URLs de la aplicación home_match #Funciona(1)
] 