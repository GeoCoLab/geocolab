from . import home, auth, applications, orgs, facilities


def init_app(app):
    blueprints = [home.bp, auth.bp, applications.bp, orgs.bp, facilities.bp]

    for bp in blueprints:
        app.register_blueprint(bp)
