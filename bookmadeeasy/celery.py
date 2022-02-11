import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTING_MODULE','bookmadeeasy.settings')

celery = Celery('bookmadeeasy')
celery.config_from_object('django.conf:settings',namespace='celery')
celery.autodiscover_tasks()