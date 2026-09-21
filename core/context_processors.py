from .models import SiteConfiguration
from django.core.cache import cache

def site_theme(request):
    def getThemeFromDB():
        # Obtenemos la configuración o usamos 'light' por defecto si aún no se ha creado
        config = SiteConfiguration.objects.first() # Solo debería haber una configuración, así que obtenemos la primera (y única) instancia
        return config.theme if config else 'light'
    theme = cache.get_or_set('daisy_site_theme', getThemeFromDB, timeout=None)
    return {'DAISY_THEME': theme}

def bandas_laterales(request):
    def getBandasFromDB():
        config = SiteConfiguration.objects.first()
        return config.bandasLaterales if config else 'rectas'
    bandas_laterales = cache.get_or_set('bandas_laterales', getBandasFromDB, timeout=None)
    return {'BANDAS_LATERALES' : bandas_laterales}