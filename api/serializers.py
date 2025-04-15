from rest_framework import serializers
from .models import TaskResult

class TaskRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()

class TaskResponseSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    status = serializers.CharField()

class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ['task_id', 'email', 'message', 'status', 'created_at', 'updated_at']
