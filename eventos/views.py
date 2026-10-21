from django.urls import reverse
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
        filtrable = request.GET.get("filtrable", self.kwargs.get("filtrable", "no"))
        self.tipo_actual = tipo if tipo in self.TIPOS_PERMITIDOS else "futuros"
        self.filtrable = filtrable if filtrable in ('si', 'no') else 'no'

    def get_queryset(self):
        # Buena práctica: Filtrar solo elementos activos y optimizar la consulta
        ahora = timezone.now()
        # Lee de query param ?tipo=... o de URLconf (self.kwargs); fallback a 'futuros'
        queryset = super().get_queryset()

        if self.tipo_actual == "futuros":
            # Eventos futuros ordenados cronológicamente (el más próximo primero)
            return queryset.filter(fecha_celebracion__gte=ahora).order_by("fecha_celebracion")
        # Eventos pasados ordenados del más reciente al más antiguo
        return queryset.filter(fecha_celebracion__lt=ahora).order_by("fecha_celebracion")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se pone a disposición del template el valor previamente validado
        context["tipo_actual"] = self.tipo_actual
        context["filtrable"] = self.filtrable
        return context
    
class EventoDetailView(DetailView):
    model = Evento
    template_name = "eventos/detalleEvento.html"
    context_object_name = "evento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Eventos", "url": reverse("eventos:eventos")},
            {"label": self.object.titulo, "url": None},            
        ]

class EventosPaginaView(ListView):
    model = Evento 
    template_name = "eventos/eventos.html"
    context_object_name = "evento"  # Variable limpia para el template

    def get_queryset(self):
        consultaBaseVista = super().get_queryset() # para respetar los posibles filtros de la clase padre en lugar de hacer Evento.objects.filter...
        return consultaBaseVista.filter(publicado=True)

    def get_context_data(self, **kwargs):
        # 1. Obtenemos el contexto base (incluye 'object' y el nombre del modelo en minúsculas)
        context = super().get_context_data(**kwargs)
        # 2. Resolver la clase del modelo de forma robusta
        model_cls = self.model if self.model is not None else self.get_queryset().model
        # 3. Inyectar la variable de clase del modelo al contexto
        categorias = [tuplaCategorias[0] for tuplaCategorias in getattr(model_cls, "CATEGORIA_CHOICES")]
        context["categorias"] = categorias
        context["breadcrumbs"] = [
            {"label": "Eventos", "url": None}            
        ]
        return context