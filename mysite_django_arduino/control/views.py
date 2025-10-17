import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .serial_service import blink_once
from .models import CommandLog

@login_required
def panel(request):
    # (opcional) mostrar últimos logs en el panel
    latest = CommandLog.objects.all()[:10]
    return render(request, 'control/panel.html', {'latest': latest})

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
