from django.views.generic import ListView, DetailView
from .models import Noticia


class NoticiasView(ListView):
    model = Noticia
    template_name = "noticias/componentes/_listaNoticias.html"
    context_object_name = "noticias"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        # Se obtiene el parámetro asegurando tipo string o fallback seguro
        valor_numero = request.GET.get("numero", self.kwargs.get("numero", "3"))
        filtrable = request.GET.get("filtrable", self.kwargs.get("filtrable", "no"))
        # Conversión segura y validación de rango (máximo 10)
        try:
            limite = int(valor_numero)
            self.numero_noticias = limite if 0 < limite <= 10 else 3
        except (ValueError, TypeError):
            self.numero_noticias = 3
        self.filtrable = filtrable if filtrable in ('si', 'no') else 'no'

    def get_queryset(self):
        # Mantiene el queryset base y aplica filtros/ordenación
        qs = super().get_queryset()
        # Se aplica el slice usando el entero calculado (genera LIMIT en SQL)
        return qs.filter(publicada=True).order_by("-fecha_publicacion")[
            : self.numero_noticias
        ]
    def get_context_data(self, **kwargs):
        # 1. Obtenemos el contexto base (incluye 'object' y el nombre del modelo en minúsculas)
        context = super().get_context_data(**kwargs)
        # 2. Obtenemos el parámetro GET de self.request y lo inyectamos al contexto
        context["filtrable"] = self.filtrable
        return context
    
class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = "noticias/detalleNoticia.html"
    context_object_name = "noticia"

class NoticiasPaginaView(ListView):
    model = Noticia # Contenido del carrousel principal
    template_name = "noticias/noticias.html"
    context_object_name = "noticias"  # Variable limpia para el template

    def get_queryset(self):
        consultaBaseVista = super().get_queryset() # para respetar los posibles filtros de la clase padre en lugar de hacer Evento.objects.filter...
        return consultaBaseVista.filter(publicada=True)

    def get_context_data(self, **kwargs):
        # 1. Obtenemos el contexto base (incluye 'object' y el nombre del modelo en minúsculas)
        context = super().get_context_data(**kwargs)
        # 2. Resolver la clase del modelo de forma robusta
        model_cls = self.model if self.model is not None else self.get_queryset().model

        # 3. Inyectar la variable de clase del modelo al contexto
        categorias = [tuplaCategorias[0] for tuplaCategorias in getattr(model_cls, "CATEGORIA_CHOICES")]
        context["categorias"] = categorias
        return context

