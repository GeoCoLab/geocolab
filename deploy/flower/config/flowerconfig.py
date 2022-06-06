import os


def get_broker_api_url():
    broker_url = os.environ.get('CELERY_BROKER_API_URL')
    if broker_url:
        return broker_url
    username = os.environ.get('RABBITMQ_DEFAULT_USER')
    password = os.environ.get('RABBITMQ_DEFAULT_PASS')
    return f'http://{username}:{password}@rabbitmq:15672/api/'


broker_api = get_broker_api_url()
