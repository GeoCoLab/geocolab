from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, mail
from . import tasks


def init(return_celery=False):
    app = Flask(__name__, static_folder=Config.STATIC_DIR, template_folder=Config.TEMPLATE_DIR, static_url_path='/static/')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    celery = tasks.init_app(app)

    from . import routes
    routes.init_app(app)

    return celery if return_celery else app


def create_app():
    return init()


def create_celery():
    return init(return_celery=True)
