from django.core.management.base import BaseCommand
from control.serial_service import blink_once

class Command(BaseCommand):
    help = "Prueba de conexión con Arduino: blink"

    def handle(self, *args, **options):
        resp = blink_once()
        self.stdout.write(self.style.SUCCESS(f"Arduino respondió: {resp}"))
