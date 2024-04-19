from celery import Celery

Cel = Celery('hello', broker='amqp://armanrasta@localhost:5672/1/')
