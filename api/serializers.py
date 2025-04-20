from rest_framework import serializers
from .models import ProcessRequest

class ProcessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessRequest
        fields = ['id', 'email', 'message', 'task_id', 'status', 'created_at']
        read_only_fields = ['task_id', 'status', 'created_at']