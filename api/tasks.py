import time
from celery import shared_task
from .models import ProcessRequest

@shared_task
def process_request_task(request_id):
    try:
        # Simulate time-consuming task
        time.sleep(10)
        
        # Update request status
        request = ProcessRequest.objects.get(id=request_id)
        request.status = 'COMPLETED'
        request.save()
        
        return {'status': 'success', 'request_id': request_id}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}