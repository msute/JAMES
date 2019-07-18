import os

from celery import Celery
from worker import config

#加入此条环境可调用django变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')

celery_app = Celery('testjames') #声明一个任务
celery_app.config_from_object(config)

celery_app.autodiscover_tasks()#自动发现惹怒
