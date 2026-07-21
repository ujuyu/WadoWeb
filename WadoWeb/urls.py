"""
URL configuration for WadoWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 1. Rutas que se mostrarán en la navegación pública
NAVBAR_URLS = [
    path('', include('core.urls'), name='home'),
]

# 2. Rutas exclusivas para peticiones interactivas / HTMX (ocultas del menú)
HTMX_URLS = [

]

# 3. Rutas de utilidad general o administración
UTILITY_URLS = [
    path('pruebas/', include('pruebas.urls')),
    path("admin/", admin.site.urls),
]

# 4. Registro de las URLS de las apps que van a servir algún contenido aunque no se navege a ellas (imprescindible)
REGISTRO_URLS = [
    path('noticias/', include('noticias.urls')),
]

# La variable que Django exige obligatoriamente
urlpatterns = NAVBAR_URLS + HTMX_URLS + UTILITY_URLS + REGISTRO_URLS

# Esta condición asegura que Django solo sirva los medios en desarrollo.
# En producción (DEBUG = False), esta regla se ignora de forma segura.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

