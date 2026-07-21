from django.views.generic import ListView
from .models import Banner

class IndexView(ListView):
    model = Banner # Contenido del carrousel principal
    template_name = "core/index.html"
    context_object_name = "banners"  # Variable limpia para el template

    def get_queryset(self):
        # Buena práctica: Filtrar solo elementos activos y optimizar la consulta
        return Banner.objects.filter(activo=True)
