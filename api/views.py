from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from celery.result import AsyncResult

from .serializers import TaskRequestSerializer, TaskResponseSerializer, TaskResultSerializer
from .tasks import process_message
from .models import TaskResult

class ProcessAPIView(APIView):
    permission_classes = [AllowAny]  # For demo purposes

    @swagger_auto_schema(
        request_body=TaskRequestSerializer,
        responses={202: TaskResponseSerializer}
    )
    def post(self, request):
        serializer = TaskRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']
            
            # Start Celery task
            task = process_message.delay(None, email, message)
            
            # Create task record
            TaskResult.objects.create(
                task_id=task.id,
                email=email,
                message=message,
                status='PENDING'
            )
            
            return Response({
                'task_id': task.id,
                'status': 'pending'
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskStatusAPIView(APIView):
    permission_classes = [AllowAny]  # For demo purposes

    @swagger_auto_schema(
        responses={200: TaskResultSerializer}
    )
    def get(self, request, task_id):
        try:
            task_result = TaskResult.objects.get(task_id=task_id)
            serializer = TaskResultSerializer(task_result)
            return Response(serializer.data)
        except TaskResult.DoesNotExist:
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
