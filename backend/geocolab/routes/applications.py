from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('apps', __name__, url_prefix='/apply')


@bp.route('/')
@login_required
def new():
    return render_template('index.html')


@bp.route('/manage')
@login_required
def manage():
    return render_template('index.html')


@bp.route('/<int:app_id>')
@login_required
def view(app_id):
    return render_template('index.html')


@bp.route('/<int:app_id>/edit')
@login_required
def edit(app_id):
    return render_template('index.html')
