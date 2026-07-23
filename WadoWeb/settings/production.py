from .base import *


DEBUG = False


# Base de datos sqlite3 con parámetros optimizados para producción
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "timeout": 30,  # Espera hasta 30s si la base de datos está ocupada antes de dar error
            "transaction_mode": "IMMEDIATE",  # Bloquea el hilo de escritura desde el inicio de la transacción
            "init_command": (
                "PRAGMA journal_mode=WAL;"  # Activa el modo WAL para permitir lecturas y escrituras simultáneas
                "PRAGMA synchronous=NORMAL;"
                "PRAGMA foreign_keys=ON;"
                "PRAGMA temp_store=MEMORY;"
            ),
        },
    }
}

# Configuración de seguridad SSL/HTTPS (obligatoria para pasarelas de pago)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Claves de Stripe en modo real (Live keys)
STRIPE_PUBLIC_KEY = 'pk_live_...'
STRIPE_SECRET_KEY = 'sk_live_...'
