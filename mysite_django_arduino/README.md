# Demo Django + Login/Registro + Arduino Blink

## Pasos rápidos (Windows PowerShell)
```powershell
# 1) Clonar/extraer y entrar a la carpeta
cd mysite_django_arduino

# 2) Entorno y paquetes
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3) Configuración
copy .env.example .env
# Edita .env (COM3/baud/SECRET_KEY)

# 4) Migrar y correr
python manage.py migrate
python manage.py runserver
```

- Registrate en `/signup/`, luego entra a `/control/`.
- Pulsa **Parpadear LED** (cierra el Monitor Serial del IDE de Arduino antes).

## Probar desde consola
```powershell
python manage.py test_serial
```

## Arduino (resumen)
- Sketch: escuchar línea; si recibe `B`, parpadea LED 13 y responde `BLINKED`.
- Velocidad por defecto: 9600 (ajusta en `.env` y en el sketch si cambias).
