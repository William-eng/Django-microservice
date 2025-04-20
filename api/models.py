from django.db import models

class ProcessRequest(models.Model):
    email = models.EmailField()
    message = models.TextField()
    task_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.status}"