from rest_framework import generics, status
from rest_framework.response import Response
from .models import ProcessRequest
from .serializers import ProcessRequestSerializer
from .tasks import process_request_task
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProcessRequestView(generics.CreateAPIView):
    serializer_class = ProcessRequestSerializer

    @swagger_auto_schema(
        operation_description="Create a new process request",
        request_body=ProcessRequestSerializer,
        responses={202: ProcessRequestSerializer()}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Start Celery task
        task = process_request_task.delay(instance.id)
        
        # Update task_id
        instance.task_id = task.id
        instance.save()
        
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class TaskStatusView(generics.RetrieveAPIView):
    queryset = ProcessRequest.objects.all()
    serializer_class = ProcessRequestSerializer
    lookup_field = 'task_id'

    @swagger_auto_schema(
        operation_description="Get the status of a process request",
        responses={200: ProcessRequestSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)