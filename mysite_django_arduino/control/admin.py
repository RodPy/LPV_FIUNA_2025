from django.contrib import admin
from .models import CommandLog,SensorData

@admin.register(CommandLog)
class CommandLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'command', 'response', 'ok', 'port', 'baud', 'duration_ms')
    list_filter = ('ok', 'port', 'baud', 'created_at')
    search_fields = ('user__username', 'command', 'response')
    date_hierarchy = 'created_at'

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('captured_at', 'sensor', 'value', 'unit', 'ok', 'user', 'port', 'baud')
    list_filter = ('ok', 'sensor', 'captured_at')
    search_fields = ('sensor', 'raw', 'user__username')
    date_hierarchy = 'captured_at'