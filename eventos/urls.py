from django.urls import path
from .views import EventosView, EventoDetailView, EventosPaginaView

app_name = "eventos"

# 1. Rutas que se mostrarán en la navegación pública
NAVEGACION_URLS = [
    path('eventos/<slug:slug>/', EventoDetailView.as_view(), name='evento_detalle'),
    path('', EventosPaginaView.as_view(), name='eventos')
]

# 2. Rutas exclusivas para peticiones interactivas / HTMX (ocultas del menú)
HTMX_URLS = [
    path('htmx/ultimos/', EventosView.as_view(), name='htmx_ultimos_eventos'),
]


# La variable que Django exige obligatoriamente
urlpatterns = NAVEGACION_URLS + HTMX_URLS