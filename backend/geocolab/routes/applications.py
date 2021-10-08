from datetime import datetime as dt

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db, login_manager
from ..forms import ApplicationForm
from ..models import Application, Analysis

bp = Blueprint('apps', __name__, url_prefix='/apply')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def new():
    form = ApplicationForm(current_location=current_user.country)
    if form.validate_on_submit():
        new_app = Application(user_id=current_user.id,
                              current_location=form.current_location.data,
                              date_from=form.date_from.data,
                              date_to=form.date_to.data,
                              reason_for_request=form.reason_for_request.data,
                              restrictions=form.restrictions.data,
                              current_org=form.current_org.data,
                              additional_requirements=form.additional_requirements.data)
        if form.is_submitted.data:
            new_app.is_submitted = True
            new_app.date_submitted = dt.now().date()
        analyses = []
        for analysis in form.analyses.data:
            analyses.append(Analysis.query.get(analysis))
        new_app.analyses = analyses
        db.session.add(new_app)
        db.session.commit()
        return redirect(url_for('apps.view', app_id=new_app.id))
    return render_template('apply/new.html', form=form)


@bp.route('/manage')
@login_required
def manage():
    return render_template('apply/manage.html')


@bp.route('/<int:app_id>')
@login_required
def view(app_id):
    application = Application.query.get(app_id)
    if not current_user.id == application.user_id:
        return login_manager.unauthorized()
    return render_template('apply/view.html', application=application)


@bp.route('/<int:app_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(app_id):
    application = Application.query.get(app_id)
    form = ApplicationForm(obj=application)
    if form.validate_on_submit():
        update_info = dict(user_id=current_user.id,
                           current_location=form.current_location.data,
                           date_from=form.date_from.data,
                           date_to=form.date_to.data,
                           reason_for_request=form.reason_for_request.data,
                           restrictions=form.restrictions.data,
                           current_org=form.current_org.data,
                           additional_requirements=form.additional_requirements.data)
        for k, v in update_info.items():
            setattr(application, k, v)
        if form.is_submitted.data and not application.is_submitted:
            application.is_submitted = True
            application.date_submitted = dt.now().date()
        analyses = []
        for analysis in form.analyses.data:
            analyses.append(Analysis.query.get(analysis))
        application.analyses = analyses
        db.session.commit()
        return redirect(url_for('apps.view', app_id=app_id))
    return render_template('apply/edit.html', form=form, application_id=app_id)
