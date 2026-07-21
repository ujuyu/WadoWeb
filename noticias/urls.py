from django.urls import path
from .views import NoticiasView, NoticiaDetailView

app_name = "noticias"

# 1. Rutas que se mostrarán en la navegación pública
NAVEGACION_URLS = [
    path('noticia/<slug:slug>/', NoticiaDetailView.as_view(), name='noticia_detalle'),
]

# 2. Rutas exclusivas para peticiones interactivas / HTMX (ocultas del menú)
HTMX_URLS = [
    path('htmx/ultimas/', NoticiasView.as_view(), name='htmx_ultimas_noticias'),
]


# La variable que Django exige obligatoriamente
urlpatterns = NAVEGACION_URLS + HTMX_URLS