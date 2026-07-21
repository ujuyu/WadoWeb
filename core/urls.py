from django.urls import path
from .views import IndexView

# Espacio de nombres (namespace) de la app. ¡Una muy buena práctica!
app_name = 'core' 

urlpatterns = [
    # Sintaxis: path('ruta-en-el-navegador/', funcion_de_la_vista, name='nombre_interno')
    path('', IndexView.as_view(), name='index'),
    
]