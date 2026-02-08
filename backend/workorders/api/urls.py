"""
Configuración de URLs para la API de workorders

Define los endpoint públicos de la app
"""

from django.urls import path
from .views import health_check, login

urlpatterns = [
  # Endpoint para verificar estado de servicio
  path('health/', health_check, name='health_check'),

  # Endpoint para autenticación de usuarios
  path('login/', login, name='login')
]