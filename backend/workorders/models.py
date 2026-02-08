"""
Puente para que Django encuentre los modelos.
Django busca automáticamente modelos en app/models.py,
así que este archivo importa y expone los modelos reales
desde infrastructure/persistence/models.py
"""

from .infrastructure.persistence.models import User, Role

__all__ = ['User', 'Role']