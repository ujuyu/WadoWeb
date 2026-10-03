from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Evento(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    tipo = models.CharField(max_length=20, verbose_name="Tipo", help_text="Jornadas, taller, curso")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug (URL)")
    resumen = models.TextField(max_length=400, verbose_name="Resumen", help_text="Texto breve que aparecerá en la página principal.")
    contenido = models.TextField(verbose_name="Contenido completo")
    imagen = models.ImageField(upload_to="eventos/%Y/%m/", verbose_name="Imagen de portada")
    plazas = models.IntegerField(verbose_name="Plazas")
    
    fecha_celebracion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de celebración")
    publicado = models.BooleanField(default=True, verbose_name="Visible al público")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos')

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-fecha_celebracion'] # Orden cronológico inverso por defecto
        indexes = [
            models.Index(fields=['-fecha_celebracion', 'publicado']),
        ]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('eventos:evento_detalle', kwargs={'slug': self.slug})


