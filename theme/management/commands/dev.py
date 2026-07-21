# theme/management/commands/dev.py

import subprocess
import sys
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Inicia el servidor de desarrollo de Django y Tailwind en modo watch simultáneamente.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando entorno de desarrollo Full-Stack...'))

        # sys.executable garantiza que usamos el Python portable de WinPython
        runserver_cmd = [sys.executable, 'manage.py', 'runserver']
        tailwind_cmd = [sys.executable, 'manage.py', 'tailwind', 'watch']

        try:
            # Popen ejecuta los procesos en paralelo sin bloquear la ejecución principal
            server_process = subprocess.Popen(runserver_cmd)
            tailwind_process = subprocess.Popen(tailwind_cmd)

            # Mantenemos el comando principal esperando a que los subprocesos terminen
            server_process.wait()
            tailwind_process.wait()

        except KeyboardInterrupt:
            # Captura cuando pulsas Ctrl+C en la consola para un cierre limpio
            self.stdout.write(self.style.WARNING('\nDeteniendo procesos...'))
            server_process.terminate()
            tailwind_process.terminate()
            self.stdout.write(self.style.SUCCESS('Procesos detenidos correctamente. ¡Hasta luego!'))