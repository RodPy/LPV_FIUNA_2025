from django.contrib import admin
from .models import CommandLog

@admin.register(CommandLog)
class CommandLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'command', 'response', 'ok', 'port', 'baud', 'duration_ms')
    list_filter = ('ok', 'port', 'baud', 'created_at')
    search_fields = ('user__username', 'command', 'response')
    date_hierarchy = 'created_at'
