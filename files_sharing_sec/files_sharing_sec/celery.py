import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','files_sharing_sec.settings')

app = Celery('files_sharing_sec')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
