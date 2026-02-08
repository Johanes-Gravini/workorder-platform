"""
Vistas para la API REST de workorders.

Una vista es una función que 
1. Recibe una petición HTTP (request)
2. Prcocesa los datos
3. Devuelve una respuesta HTTP (request)

En este archivo:
- health_check: Endpoint para verificar que la API funciona
- login: Endpoint para autenticar usuarios y generar tokens JWT
"""
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

def health_check(request):
  """
  Endpoint para verificar que la API está funcionando.
    
  URL: GET /api/health/
  Respuesta: {"status": "ok"}
  """
  return JsonResponse({"status": "ok"})

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
  """
  Autentica a un usuario y genera tokens JWT.
  
  Método: POST
  URL: /api/login/
  
  Body (JSON):
    {
      "username": "string",
      "password": "string"
    }
  
  Retorna:
    JsonResponse (200 OK):
      {
        "success": true,
        "data": {
          "access": "string",      # Token de acceso (1h)
          "refresh": "string",     # Token de refresh (7d)
          "user": {
            "id": int,
            "username": "string",
            "email": "string",
            "role": "string|null"
          }
        }
      }
      
    JsonResponse (401 Unauthorized):
      {
        "success": false,
        "error": {
          "code": 401,
          "message": "string",
          "details": {}
        }
      }
  """
  serializer = LoginSerializer(data=request.data, context={"request": request})
  
  if not serializer.is_valid():
    return JsonResponse({
      "success": False,
      "error": {
        "code": status.HTTP_401_UNAUTHORIZED,
        "message": "No se puede iniciar sesión con las credenciales proporcionadas.",
        "details": serializer.errors
      }
    }, status=status.HTTP_401_UNAUTHORIZED)
  
  user = serializer.validated_data["user"]
  refresh = RefreshToken.for_user(user)
  
  user_data = {
    "id": user.id,
    "username": user.username,
    "email": user.email,
    "role": user.role.name if user.role else None
  }
  
  return JsonResponse({
    "success": True,
    "data": {
      "access": str(refresh.access_token),
      "refresh": str(refresh),
      "user": user_data
    }
  }, status=status.HTTP_200_OK)