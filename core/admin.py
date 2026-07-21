from django.contrib import admin
from django.utils.html import format_html
from .models import SiteConfiguration # Importa el modelo de configuración del sitio para registrarlo en el admin de Django
from .models import Banner

@admin.register(SiteConfiguration) # Registra el modelo en el admin de Django usando un decorador para una sintaxis más limpia
class SiteConfigurationAdmin(admin.ModelAdmin):
    # Desactiva el botón de "Añadir" si ya existe una configuración
    def has_add_permission(self, request): # Sobrescribe el método para controlar los permisos de añadir nuevos registros
        if self.model.objects.exists(): # Si ya existe una configuración, no permite añadir otra
            return False
        return super().has_add_permission(request) # Llama al método original para mantener el comportamiento por defecto en otros casos


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Banner.
    Eficiencia: Permite editar 'orden' y 'activo' directamente desde el listado sin entrar al detalle.
    """
    # Columnas visibles en el listado
    list_display = ('titulo', 'orden', 'imagen', 'activo')
    
    # Campos que se pueden editar directamente en la tabla
    list_editable = ('orden', 'activo')
    
    # Filtros laterales
    list_filter = ('activo',)
    
    # Barra de búsqueda
    search_fields = ('titulo', 'descripcion')
    
    # Ordenamiento por defecto en el admin
    ordering = ('orden',)
