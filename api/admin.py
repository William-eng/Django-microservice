from django.contrib import admin
from .models import ProcessRequest


@admin.register(ProcessRequest)
class ProcessRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'created_at', 'task_id')
    list_filter = ('status', 'created_at')
    search_fields = ('email', 'message', 'task_id')