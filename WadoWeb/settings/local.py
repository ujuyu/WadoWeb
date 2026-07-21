from .base import *
from .base import BASE_DIR

# Activar modo depuración para ver errores en pantalla
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de datos SQLite local para desarrollo rápido
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Claves de Stripe en modo pruebas (Test keys)
STRIPE_PUBLIC_KEY = 'pk_test_...'
STRIPE_SECRET_KEY = 'sk_test_...'