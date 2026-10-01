from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField" # tipo de clave primaria automática que se asignará implícitamente a los modelos
    name = "core" # app a la que aplica esta configuración 
    verbose_name = _('Página principal') # nombre aplicable a la interfaz de administración
