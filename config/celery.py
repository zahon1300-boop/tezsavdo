"""
Celery configuration for TezSavdo
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Beat Schedule (Periodic Tasks)
app.conf.beat_schedule = {
    'cleanup-sessions': {
        'task': 'shop.tasks.cleanup_sessions',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM UTC
    },
    'send-daily-reports': {
        'task': 'shop.tasks.send_daily_reports',
        'schedule': crontab(hour=8, minute=0),  # Daily at 8 AM UTC
    },
    'update-product-cache': {
        'task': 'shop.tasks.update_product_cache',
        'schedule': crontab(hour='*/4', minute=0),  # Every 4 hours
    },
}

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery connectivity"""
    print(f'Request: {self.request!r}')
