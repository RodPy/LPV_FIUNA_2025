from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .serial_service import blink_once

@login_required
def panel(request):
    return render(request, 'control/panel.html')

@login_required
def do_blink(request):
    if request.method == 'POST':
        try:
            resp = blink_once()
            messages.success(request, f'Comando enviado. Respuesta: {resp}')
        except Exception as e:
            messages.error(request, f'No se pudo comunicar con Arduino: {e}')
    return redirect('panel')
