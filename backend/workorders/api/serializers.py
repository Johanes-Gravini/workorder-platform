"""
Serializadores para la API de workorders.

Este módulo contiene serializadores para validar y transformar 
datos entre JSON (frontend) y objetos Python (backend)
"""

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
  """
  Serializador para el login de usuarios.

  Valida las credenciales de username y password y autentica al usuario.

  Ejemplo de petición:
    {
      "username": "string",
      "password": "string"
    }
  
  Lanza:
    ValidationError: si las credenciales son inválidas o el usuario no está activo.
  """
  username = serializers.CharField(
    label=_("Username"),
    max_length=150,
    help_text=_("Requerido. 1-150 caracteres.")
  )
  
  password = serializers.CharField(
    label=_("Password"),
    style={"input_type": "password"},
    trim_whitespace=True,
    help_text=_("Requerido. Contraseña del usuario.")
  )

  def validate(self, attrs):
    """
    Valida las credenciales del usuario.

    Args:
      attrs (dict): Diccionario con 'username' y 'password'.
    
    Returns:
      dict: Atributos validados con el objeto de usuario autenticado.

    Raises:
      serializers.ValidationError: Si la autenticación falla.
    """
    username = attrs.get("username")
    password = attrs.get("password")

    if username and password:
      # Intentamos autenticar al usuario con Django
      user = authenticate(
        request=self.context.get("request"),
        username=username,
        password=password
      )

      # Si la autenticación falla
      if not user:
        msg = _("No se puede iniciar sesión con las credenciales proporcionadas.")
        raise serializers.ValidationError(msg, code="authorization")

      # Si el usuario está desactivado
      if not user.is_active:
        msg = _("La cuenta de usuario está desactivada.")
        raise serializers.ValidationError(msg, code="authorization")
    
    else:
      # Si falta username o password
      msg = _('Debe incluir "username" y "password".')
      raise serializers.ValidationError(msg, code="authorization")

    # Guardamos el usuario en los atributos validados
    attrs["user"] = user
    return attrs