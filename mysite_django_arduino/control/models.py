from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SensorData(models.Model):
    # Quién solicitó la lectura (opcional, útil para auditoría)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sensor_reads')

    # Identificador lógico del sensor (ej: "TEMP", "HUM", "LIGHT", "A0", etc.)
    sensor = models.CharField(max_length=50)

    # Valor numérico de la lectura (usa Decimal para precisión)
    value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)

    # Unidad opcional (ej: "C", "%", "lx", "mV")
    unit = models.CharField(max_length=20, blank=True)

    # Puerto/baud utilizados (para trazabilidad)
    port = models.CharField(max_length=50, blank=True)
    baud = models.IntegerField(default=9600)

    # Respuesta cruda recibida por serial (útil para debug)
    raw = models.TextField(blank=True)

    # Éxito del parseo/lectura
    ok = models.BooleanField(default=False)

    # Extra (JSON opcional: rangos, calibres, tags, etc.)
    # Si tu versión de Django es 3.1+:
    metadata = models.JSONField(null=True, blank=True)

    # Timestamps
    captured_at = models.DateTimeField(auto_now_add=True)  # cuándo se capturó
    created_at = models.DateTimeField(auto_now_add=True)   # redundante pero útil si deseas distinguir

    class Meta:
        ordering = ['-captured_at']
        indexes = [
            models.Index(fields=['captured_at']),
            models.Index(fields=['sensor']),
            models.Index(fields=['ok']),
        ]

    def __str__(self):
        status = "OK" if self.ok else "ERR"
        return f"[{self.captured_at:%Y-%m-%d %H:%M:%S}] {self.sensor}={self.value}{self.unit or ''} ({status})"
class CommandLog(models.Model):
    # Usuario que ejecutó el comando (nullable por si querés registrar tareas de sistema)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='arduino_commands')

    # Datos del comando
    command = models.CharField(max_length=50)                 # ej: "B"
    response = models.CharField(max_length=255, blank=True)   # ej: "BLINKED"
    ok = models.BooleanField(default=False)                   # True si la respuesta fue la esperada

    # Info del hardware (opcional, útil para auditoría)
    port = models.CharField(max_length=50, blank=True)        # ej: "COM3" o "/dev/ttyACM0"
    baud = models.IntegerField(default=9600)

    # Métrica de tiempo
    duration_ms = models.PositiveIntegerField(default=0)      # tiempo total del request (aprox)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['ok']),
        ]

    def __str__(self):
        u = self.user.username if self.user else "system"
        return f"[{self.created_at:%Y-%m-%d %H:%M:%S}] {u} -> {self.command} ({'OK' if self.ok else 'ERR'})"
