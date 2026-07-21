from django.urls import path
from . import views  # Importa las vistas de esta misma aplicación

# Espacio de nombres (namespace) de la app. ¡Una muy buena práctica!
app_name = 'pruebas' 

urlpatterns = [
    # Sintaxis: path('ruta-en-el-navegador/', funcion_de_la_vista, name='nombre_interno')
    
    # Ejemplo 1: La ruta principal de esta app (ej. misitio.com/laboratorio/)
    path('', views.index, name='inicio'),
    
]