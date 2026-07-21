from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Noticia(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug (URL)")
    resumen = models.TextField(max_length=400, verbose_name="Resumen", help_text="Texto breve que aparecerá en la página principal.")
    contenido = models.TextField(verbose_name="Contenido completo")
    imagen = models.ImageField(upload_to="noticias/%Y/%m/", verbose_name="Imagen de portada")
    
    fecha_publicacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de publicación")
    publicada = models.BooleanField(default=True, verbose_name="Visible al público")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='noticias')

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ['-fecha_publicacion'] # Orden cronológico inverso por defecto
        indexes = [
            models.Index(fields=['-fecha_publicacion', 'publicada']),
        ]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('noticias:noticia_detalle', kwargs={'slug': self.slug})

# Create your models here.
