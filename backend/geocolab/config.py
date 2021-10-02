import os

from dotenv import load_dotenv

root = os.environ.get('ROOT_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

load_dotenv(os.path.join(root, '.env'))


class Config(object):
    DEBUG = os.environ.get('FLASK_DEBUG', 0) == 1
    TEMPLATES_AUTO_RELOAD = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('FLASK_SECRET') or 'E+k9{x3gB^VE_3.r'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET')

    ROOT_DIR = root
    STATIC_DIR = os.environ.get('STATIC_DIR', os.path.join(root, 'frontend', 'static'))
    TEMPLATE_DIR = os.environ.get('TEMPLATE_DIR', os.path.join(STATIC_DIR, 'templates'))

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql+psycopg2://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'geocolab.app@gmail.com'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'geocolab.app@gmail.com'

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULTS_BACKEND')
