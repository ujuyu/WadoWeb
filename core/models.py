from django.db import models
from django.core.exceptions import ValidationError 
from django.core.cache import cache

class SiteConfiguration(models.Model): # Las bases de datos solo viven en las Apps, no en el proyecto
    # Añade aquí los temas de DaisyUI que quieras permitir
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('cupcake', 'Cupcake'),
        ('bumblebee', 'Bumblebee'),
        ('corporate', 'Corporate'),
        ('synthwave', 'Synthwave'),
    ]
    
    theme = models.CharField(
        max_length=50, 
        choices=THEME_CHOICES, # Asegura que solo se puedan elegir temas válidos
        default='light', # Establece un tema por defecto
        verbose_name="Tema visual" # Nombre legible para el campo en el admin de Django
    )

    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuración del Sitio"

    def save(self, *args, **kwargs):
        # Asegura que solo exista un registro en la base de datos
        if not self.pk and SiteConfiguration.objects.exists(): # Si ya existe una configuración, no permite crear otra
            raise ValidationError('Solo puede existir una configuración del sitio.') 
        super().save(*args, **kwargs) # Llama al método save original para guardar el registro
        # Esto hay que hacerlo para todas las columnas del SiteConfiguracion pues estarán todas cacheadas
        cache.delete('daisy_site_theme')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Limpiamos la caché si se elimina el registro por algún motivo.
        cache.delete('daisy_site_theme')


    def __str__(self):
        return "Configuración Global" # Representación legible del objeto en el admin de Django
    
class Banner(models.Model):
    titulo = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="carrouselPortada/%Y/%m/", verbose_name="Imagen del carrousel")
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.titulo