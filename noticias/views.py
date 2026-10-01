from django.views.generic import ListView, DetailView
from .models import Noticia

class NoticiasView(ListView):
    model = Noticia # Contenido del carrousel principal
    template_name = "noticias/componentes/_listaNoticias.html"
    context_object_name = "noticias"  # Variable limpia para el template

    def get_queryset(self):
        consultaBaseVista = super().get_queryset() # para respetar los posibles filtros de la clase padre en lugar de hacer Evento.objects.filter...
        return consultaBaseVista.filter(publicada=True)
    
class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = "noticias/detalleNoticia.html"
    context_object_name = "noticia"


