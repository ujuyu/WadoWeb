from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Evento

class EventosView(ListView):
    model = Evento
    template_name = "eventos/componentes/_listaEventos.html"
    context_object_name = "eventos"  # Variable limpia para el template
    TIPOS_PERMITIDOS = {"pasados", "futuros"} # atributo de clase

    def setup(self, request, *args, **kwargs): # para poder pedir eventos ?pasados o ?futuros
        super().setup(request, *args, **kwargs)
        tipo = request.GET.get("tipo", self.kwargs.get("tipo", "futuros"))
        self.tipo_actual = tipo if tipo in self.TIPOS_PERMITIDOS else "futuros"

    def get_queryset(self):
        # Buena práctica: Filtrar solo elementos activos y optimizar la consulta
        ahora = timezone.now()
        # Lee de query param ?tipo=... o de URLconf (self.kwargs); fallback a 'futuros'
        queryset = super().get_queryset()

        if self.tipo_actual == "futuros":
            # Eventos futuros ordenados cronológicamente (el más próximo primero)
            return queryset.filter(fecha_celebracion__gte=ahora).order_by("fecha_celebracion")
        # Eventos pasados ordenados del más reciente al más antiguo
        return queryset.filter(fecha_celebracion__lt=ahora).order_by("-fecha_celebracion")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se pone a disposición del template el valor previamente validado
        context["tipo_actual"] = self.tipo_actual
        return context
    
class EventoDetailView(DetailView):
    model = Evento
    template_name = "noticias/detalleNoticia.html"
    context_object_name = "noticia"