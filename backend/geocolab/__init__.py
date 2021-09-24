from flask import Flask
from geocolab.config import Config
from geocolab.extensions import db, migrate, jwt, mail
from geocolab import tasks


def init(return_celery=False):
    app = Flask(__name__, static_folder=Config.STATIC_DIR)
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
