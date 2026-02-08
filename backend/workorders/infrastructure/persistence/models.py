"""
Archivo: models.py
Propósito: Define los modelos de base de datos para la aplicación workorders

En Django cada clase representa una tabla, y cada atributo de la clase representa 
una columna 

Por ejemplo: 
- la Clase User crea una tabla llamada 'users' en la base de datos
- el atributo 'username' crea una columna llamada 'username' en esa tabla
"""

# Importamos las clases base de Django para crear modelos
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

"""
Modelo para representar los roles de usuarios en el sistema.

esto crea una tabla llamada 'roles' en la base de datos con estos campos:
- id: número autoincrementable (creado automáticamente por Django)
- name: nombre del rol
- description: descripción opcional del rol
"""
class Role(models.Model):
  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=True)

  # constantes para los nombre de los roles
  ADMIN = 'admin'
  SUPERVISOR = 'supervisor'
  TECHNICIAN = 'technician'
  CLIENT = 'client'

  """
  Clase meta: Configuración adicional para el modelo.
  No crea campos en la BD, solo configura cómo se comporta el modelo
  """
  class Meta:
    db_table = 'roles' # Nombre de la tabla en la base de datos
    verbose_name = 'Role' # Nombre en singular para mostrar en el admin
    verbose_name_plural = 'Roles' # Nombre en plural para mostrar en el admin

  """
  Método que define cómo se muestra este objeto cuando lo convertimos a texto.
  Por ejemplo, en el panel de administración de Django, se mostrará el nombre del rol.
  """
  def __str__(self):
    return self.name

"""
Modelo de usuario personalizado.

Heredamos de AbstractUser, que es el modelo de usuario básico de Django.
Esto significa que nuestro User ya tiene todos los campos básicos:
- username, password, email, first_name, last_name, etc.
- Métodos para autenticación, permisos, etc.

Solo agregamos campos adicionales específicos para nuestro sistema.

Esto crea una tabla llamada 'users' en la base de datos.
"""
class User(AbstractUser):
  # Campo de relación: cada usuario puede tener UN rol
  # ForeignKey - conecta esta tabla con la tabla 'roles'
  role = models.ForeignKey(
    Role,
    on_delete=models.SET_NULL, # Si se elimina el rol, ponemos NULL en el usuario
    null=True,
    blank=True,
    related_name='users',
  )
  phone = models.CharField(max_length=20, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  """
  Clase Meta: Configuración adicional para el modelo.
  No crea campos en la BD, solo configura cómo se comporta el modelo
  """
  class Meta:
    db_table = 'users'
    verbose_name = 'User'  # Nombre en singular
    verbose_name_plural = 'Users'  # Nombre en plural
  
  """
  Cómo se muestra el usuario como texto.
  Ejemplo: "juan (technician)" o "maria (supervisor)"
  """
  def __str__(self):
    # Si el usuario tiene un rol, lo mostramos junto al username
    if self.role:
        return f"{self.username} ({self.role.name})"
    # Si no tiene rol, solo mostramos el username
    return self.username