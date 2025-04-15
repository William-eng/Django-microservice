from django.urls import path
from .views import ProcessAPIView, TaskStatusAPIView

urlpatterns = [
    path('process/', ProcessAPIView.as_view(), name='process'),
    path('status/<str:task_id>/', TaskStatusAPIView.as_view(), name='task_status'),
]
