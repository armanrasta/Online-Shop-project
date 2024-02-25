from celery import Celery

CeleryApp = Celery('hello', broker='amqp://armanrasta@localhost:5672/1/')
