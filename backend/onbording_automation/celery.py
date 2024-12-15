import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onbording_automation.settings')
app = Celery("onbording_automation")
app.config_from_object("django.conf:settings", namespace = "CELERY")
app.autodiscover_tasks()
