from django.contrib import admin
from .models import Noticia
# Register your models here.
'''
Un punto (.): Directorio actual.
Dos puntos (..): El directorio padre (sube un nivel en la jerarquía de carpetas).
Tres puntos (...): El directorio abuelo (sube dos niveles), y así sucesivamente.
'''

admin.site.register(Noticia)