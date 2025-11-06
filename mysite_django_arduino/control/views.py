import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .serial_service import blink_once, read_sensor as read_sensor_cmd
from .models import SensorData, CommandLog  # CommandLog es opcional si lo añadiste antes
from .models import CommandLog

@login_required
def panel(request):
    latest_cmds = []
    try:
        latest_cmds = CommandLog.objects.all()[:10]
    except Exception:
        pass
    latest_data = SensorData.objects.all()[:10]
    return render(request, 'control/panel.html', {
        'latest_cmds': latest_cmds,
        'latest_data': latest_data,
    })
@login_required
def do_blink(request):
    if request.method == 'POST':
        t0 = time.perf_counter()
        command = "B"
        response = ""
        ok = False
        try:
            response = blink_once()
            ok = (response.strip().upper() == "BLINKED")
            messages.success(request, f'Comando enviado. Respuesta: {response}')
        except Exception as e:
            response = f"ERROR: {e}"
            messages.error(request, f'No se pudo comunicar con Arduino: {e}')
        finally:
            duration_ms = int((time.perf_counter() - t0) * 1000)
            CommandLog.objects.create(
                user=request.user,
                command=command,
                response=response[:255],
                ok=ok,
                port=getattr(settings, 'ARDUINO_PORT', ''),
                baud=int(getattr(settings, 'ARDUINO_BAUD', 9600)),
                duration_ms=duration_ms,
            )
    return redirect('panel')

def read_sensor_view(request, sensor: str):
    """
    Ejecuta lectura de un sensor (ej: TEMP, HUM, A0) y guarda en SensorData.
    """
    if request.method == 'POST':
        t0 = time.perf_counter()
        result = {"ok": False, "value": None, "unit": "", "raw": ""}
        try:
            result = read_sensor_cmd(sensor)
            messages.success(request, f"{sensor}: {result['value']} {result['unit']}" if result['ok'] else f"Lectura {sensor} falló")
        except Exception as e:
            messages.error(request, f"Error al leer {sensor}: {e}")
        finally:
            duration_ms = int((time.perf_counter() - t0) * 1000)

            SensorData.objects.create(
                user=request.user,
                sensor=sensor.upper(),
                value=result['value'],
                unit=result['unit'] or "",
                ok=result['ok'],
                port=getattr(settings, 'ARDUINO_PORT', ''),
                baud=int(getattr(settings, 'ARDUINO_BAUD', 9600)),
                raw=(result['raw'] or "")[:2000],  # evita cadenas enormes
                # captured_at auto
            )
    return redirect('panel')