from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Evento, Actividad


class EventosView(ListView):
    model = Evento
    template_name = "eventos/componentes/_listaEventos.html"
    context_object_name = "eventos"  # Variable limpia para el template
    TIPOS_PERMITIDOS = {"pasados", "futuros"}  # atributo de clase

    def setup(self, request, *args, **kwargs):  # para poder pedir eventos ?pasados o ?futuros
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
            return queryset.filter(fecha_inicio__gte=ahora).order_by("fecha_inicio")
        # Eventos pasados ordenados del más reciente al más antiguo
        return queryset.filter(fecha_inicio__lt=ahora).order_by("fecha_inicio")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se pone a disposición del template el valor previamente validado
        context["tipo_actual"] = self.tipo_actual
        context["filtrable"] = self.filtrable
        return context


class ActividadesEventoView(ListView):
    model = Actividad
    template_name = "eventos/componentes/_listaActividades.html"
    context_object_name = "actividades"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.fecha_param = request.GET.get("fecha", "")
        turno = request.GET.get("turno", "")
        filtrable = request.GET.get("filtrable", "no")
        self.turno_actual = turno if turno in ("manana", "tarde") else ""
        self.filtrable = filtrable if filtrable in ("si", "no") else "no"

    def get_queryset(self):
        qs = super().get_queryset().filter(evento__slug=self.kwargs.get("slug")).order_by("fecha_celebracion")
        actividades = list(qs)
        resultado = []
        for act in actividades:
            fecha_local = timezone.localtime(act.fecha_celebracion) if timezone.is_aware(act.fecha_celebracion) else act.fecha_celebracion
            if self.fecha_param and fecha_local.strftime("%Y-%m-%d") != self.fecha_param:
                continue
            if self.turno_actual == "manana" and fecha_local.hour >= 15:
                continue
            if self.turno_actual == "tarde" and fecha_local.hour < 15:
                continue
            resultado.append(act)
        return resultado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtrable"] = self.filtrable
        context["turno_actual"] = self.turno_actual
        context["fecha_actual"] = self.fecha_param
        return context


class EventoDetailView(DetailView):
    model = Evento
    template_name = "eventos/detalleEvento.html"
    context_object_name = "evento"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("actividades")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actividades = list(self.object.actividades.all().order_by("fecha_celebracion"))
        tiene_actividades = len(actividades) > 0

        dias_actividades = []
        for act in actividades:
            fecha_local = timezone.localtime(act.fecha_celebracion) if timezone.is_aware(act.fecha_celebracion) else act.fecha_celebracion
            dia = fecha_local.date()
            if dia not in dias_actividades:
                dias_actividades.append(dia)

        categorias_actividad = [tupla[0] for tupla in getattr(Actividad, "CATEGORIA_CHOICES")]

        context["tiene_actividades"] = tiene_actividades
        context["dias_actividades"] = dias_actividades
        context["categorias_actividad"] = categorias_actividad
        context["breadcrumbs"] = [
            {"label": "Eventos", "url": reverse("eventos:eventos")},
            {"label": self.object.titulo, "url": None},
        ]
        return context


class EventosPaginaView(ListView):
    model = Evento
    template_name = "eventos/eventos.html"
    context_object_name = "evento"  # Variable limpia para el template

    def get_queryset(self):
        consultaBaseVista = super().get_queryset()  # para respetar los posibles filtros de la clase padre en lugar de hacer Evento.objects.filter...
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
