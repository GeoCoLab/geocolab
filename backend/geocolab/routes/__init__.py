from . import home, auth


def init_app(app):
    blueprints = [home.bp, auth.bp]

    for bp in blueprints:
        app.register_blueprint(bp)
