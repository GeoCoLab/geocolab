import click
from flask.cli import FlaskGroup
from geocolab.extensions import db
from geocolab import create_app


def create_cli_app(info):
    app = create_app()

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}

    return app


@click.group(cls=FlaskGroup, create_app=create_cli_app)
def cli():
    """
    CLI for geocolab.
    """
    pass


if __name__ == '__main__':
    cli()
