import os
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

def rutaImagenActividad(instance, filename):
    """
    Devuelve la ruta de guardado con la carpeta del evento
    al que está adscrita: eventos/<slug-del-evento>/fecha/<archivo>
    """
    evento = instance.evento
    carpeta = slugify(evento.slug or evento.titulo) or f"evento-{evento.pk}"
    return f"eventos/{carpeta}/{filename}"


class Evento(models.Model):
    CATEGORIA_CHOICES = [('Taller', 'Taller'), ('Jornadas', 'Jornadas'), ('Charla', 'Charla'), ('Curso', 'Curso')]
    titulo = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug (URL)")
    resumen = models.TextField(max_length=400, verbose_name="Resumen", help_text="Texto breve que aparecerá en la página principal.")
    contenido = models.TextField(verbose_name="Contenido completo")
    imagen = models.ImageField(upload_to="eventos/%Y/%m/", verbose_name="Imagen de portada")
    plazas = models.IntegerField(default=0, verbose_name="Plazas disponibles")
    plazasUtilizadas = models.IntegerField(default=0, verbose_name="Plazas utilizadas", help_text="Rellenar solo si se quieren reservar plazas sin inscripción")
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='Jornadas'
    )

    fecha_inicio = models.DateTimeField(default=timezone.now, verbose_name="Fecha de inicio")
    fecha_finalizacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de finalización")
    publicado = models.BooleanField(default=True, verbose_name="Visible al público")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos')

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-fecha_inicio']  # Orden cronológico inverso por defecto
        indexes = [
            models.Index(fields=['-fecha_inicio', 'publicado']),
        ]

    @property
    def fecha_celebracion(self):
        """Compatibilidad con plantillas que consulten fecha_celebracion."""
        return self.fecha_inicio

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('eventos:evento_detalle', kwargs={'slug': self.slug})


class Actividad(models.Model):
    CATEGORIA_CHOICES = [
        ('Rol', 'Rol'),
        ('Juegos de mesa', 'Juegos de mesa'),
        ('Taller', 'Taller'),
        ('Charla', 'Charla'),
        ('Torneo', 'Torneo'),
        ('Otros', 'Otros'),
    ]
    titulo = models.CharField(max_length=200, verbose_name="Título")
    resumen = models.TextField(max_length=400, verbose_name="Resumen")
    contenido = models.TextField(verbose_name="Descripción")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="actividades")
    imagen = models.ImageField(upload_to=rutaImagenActividad, verbose_name="Imagen")
    plazas = models.IntegerField(default=0, verbose_name="Plazas disponibles")
    plazasUtilizadas = models.IntegerField(default=0, verbose_name="Plazas utilizadas", help_text="Rellenar solo si se quieren reservar plazas sin inscripción")
    autor = models.CharField(max_length=100, verbose_name="Autor")
    edadMinima = models.IntegerField(default=0, verbose_name="Edad mínima")
    lugar = models.CharField(max_length=200, verbose_name="Lugar")
    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIA_CHOICES,
        default='Taller',
        verbose_name="Tipo de actividad"
    )
    fecha_celebracion = models.DateTimeField(default=timezone.now, verbose_name="Fecha y hora de celebración")

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ['fecha_celebracion']

    @property
    def turno(self):
        fecha_local = timezone.localtime(self.fecha_celebracion) if timezone.is_aware(self.fecha_celebracion) else self.fecha_celebracion
        return "manana" if fecha_local.hour < 15 else "tarde"

    def __str__(self):
        return f"{self.titulo} ({self.evento.titulo})"