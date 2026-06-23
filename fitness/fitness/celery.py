import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness.settings')

app = Celery('fitness')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps
app.autodiscover_tasks()

# ─── Periodic Tasks Schedule ──────────────────────────────────────────────────
app.conf.beat_schedule = {
    'expire-subscriptions-daily': {
        'task': 'store.tasks.check_expired_subscriptions',
        'schedule': crontab(hour=0, minute=1),  # Run daily at 12:01 AM
    },
    'send-class-reminders-hourly': {
        'task': 'notifications.tasks.send_class_reminders',
        'schedule': crontab(minute=0),  # Run every hour
    },
}

app.conf.timezone = 'Asia/Kolkata'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
