from . import home


def init_app(app):
    blueprints = [home.bp]

    for bp in blueprints:
        app.register_blueprint(bp)
