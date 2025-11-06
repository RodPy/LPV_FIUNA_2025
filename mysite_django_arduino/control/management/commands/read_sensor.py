from django.core.management.base import BaseCommand
from django.conf import settings
from control.serial_service import read_sensor
from control.models import SensorData

class Command(BaseCommand):
    help = "Lee un sensor y guarda en SensorData. Uso: python manage.py read_sensor TEMP"

    def add_arguments(self, parser):
        parser.add_argument('sensor', type=str, help='Nombre del sensor, ej: TEMP, HUM, A0')

    def handle(self, *args, **opts):
        sensor = opts['sensor']
        res = read_sensor(sensor)
        self.stdout.write(str(res))
        SensorData.objects.create(
            user=None,  # sistema
            sensor=sensor.upper(),
            value=res['value'],
            unit=res['unit'] or "",
            ok=res['ok'],
            port=getattr(settings, 'ARDUINO_PORT', ''),
            baud=int(getattr(settings, 'ARDUINO_BAUD', 9600)),
            raw=(res['raw'] or "")[:2000],
        )
        self.stdout.write(self.style.SUCCESS("Guardado en SensorData."))
