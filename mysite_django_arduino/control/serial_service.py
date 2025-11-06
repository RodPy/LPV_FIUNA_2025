import time
import serial
import threading
from django.conf import settings

_lock = threading.Lock()
_ser = None

def _open_serial():
    s = serial.Serial(settings.ARDUINO_PORT, settings.ARDUINO_BAUD, timeout=1)
    time.sleep(2)  # reset del Arduino
    return s

def get_serial():
    global _ser
    if _ser and _ser.is_open:
        return _ser
    with _lock:
        if _ser and _ser.is_open:
            return _ser
        _ser = _open_serial()
        return _ser

def send_line(text: str, expect_line: bool = True) -> str:
    ser = get_serial()
    data = (text.strip() + "\n").encode("utf-8", "ignore")
    ser.write(data)
    ser.flush()
    if expect_line:
        try:
            resp = ser.readline().decode("utf-8", "ignore").strip()
        except Exception:
            resp = ""
        return resp
    return ""

def blink_once():
    resp = send_line("B", expect_line=True)
    return resp or "OK"

def read_sensor(sensor: str):
    """
    Envía 'READ:<sensor>' y espera un formato:
        SENSOR:<sensor>;VALUE:<numero>;UNIT:<unidad>
    Retorna dict con parseo y crudo.
    """
    raw = send_line(f"READ:{sensor}", expect_line=True)
    ok, value, unit = False, None, ""
    try:
        # Parsing súper simple; ajusta según tu protocolo real
        # Ej: "SENSOR:TEMP;VALUE:23.45;UNIT:C"
        parts = dict(
            kv.split(":", 1) for kv in (seg.strip() for seg in raw.split(";")) if ":" in kv
        )
        if parts.get("SENSOR", "").upper() == sensor.upper():
            val_txt = parts.get("VALUE")
            unit = parts.get("UNIT", "")
            if val_txt is not None:
                value = float(val_txt)
                ok = True
    except Exception:
        ok = False
    return {"ok": ok, "value": value, "unit": unit, "raw": raw}
