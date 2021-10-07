from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..forms import OrgForm
from ..models import Org
from ..extensions import db

bp = Blueprint('orgs', __name__, url_prefix='/orgs')


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = OrgForm()
    if form.validate_on_submit():
        ror_id = form.ror_id.data
        if ror_id:
            ror_id = ror_id[-9:]
        new_org = Org(name=form.name.data, country=form.country.data, ror_id=ror_id)
        new_org.managers.append(current_user)
        db.session.add(new_org)
        db.session.commit()
        return redirect(url_for('orgs.view', org_id=new_org.id))
    return render_template('orgs/new.html', form=form)


@bp.route('/manage')
@login_required
def manage():
    return render_template('orgs/manage.html')


@bp.route('/<int:org_id>')
@login_required
def view(org_id):
    org = Org.query.get(org_id)
    return render_template('orgs/view.html', org=org)


@bp.route('/<int:org_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(org_id):
    org = Org.query.get(org_id)
    form = OrgForm(obj=org)
    if form.validate_on_submit():
        ror_id = form.ror_id.data
        if ror_id:
            ror_id = ror_id[-9:]
        org.name = form.name.data
        org.ror_id = ror_id
        org.country = form.country.data
        db.session.commit()
        return redirect(url_for('orgs.view', org_id=org_id))
    return render_template('orgs/edit.html', form=form, org_id=org_id)
