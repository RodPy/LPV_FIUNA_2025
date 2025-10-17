from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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
