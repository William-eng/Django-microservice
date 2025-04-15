import time
import logging
from celery import shared_task
from .models import TaskResult

logger = logging.getLogger(__name__)

@shared_task
def process_message(task_id, email, message):
    try:
        # Get or create task result
        task_result, created = TaskResult.objects.get_or_create(
            task_id=task_id,
            defaults={'email': email, 'message': message, 'status': 'PROCESSING'}
        )
        
        if not created:
            task_result.status = 'PROCESSING'
            task_result.save()
        
        # Simulate time-consuming operation
        logger.info(f"Processing task {task_id} for {email}")
        time.sleep(10)  # Simulate work
        
        # Update task status
        task_result.status = 'COMPLETED'
        task_result.save()
        
        logger.info(f"Task {task_id} completed successfully")
        return {'status': 'completed', 'task_id': task_id}
    
    except Exception as e:
        logger.error(f"Error processing task {task_id}: {str(e)}")
        
        # Update task status to failed
        task_result = TaskResult.objects.get(task_id=task_id)
        task_result.status = 'FAILED'
        task_result.save()
        
        return {'status': 'failed', 'task_id': task_id, 'error': str(e)}
