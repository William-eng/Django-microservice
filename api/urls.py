from django.urls import path
from .views import ProcessRequestView, TaskStatusView

urlpatterns = [
    path('process/', ProcessRequestView.as_view(), name='process-request'),
    path('status/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
]