from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from ..extensions import db
from ..forms import FacilityForm
from ..models import Facility, Slot, Analysis

bp = Blueprint('facs', __name__, url_prefix='/facilities')


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form_defaults = {}
    if 'org' in request.args:
        form_defaults['org'] = request.args['org']
    form = FacilityForm(**form_defaults)
    if form.validate_on_submit():
        new_facility = Facility(name=form.name.data, notes=form.notes.data,
                                org_id=form.org.data)
        db.session.add(new_facility)
        analyses = []
        for analysis in form.analyses.data:
            analyses.append(Analysis.query.get(analysis))
        new_facility._analyses = analyses
        db.session.commit()
        for i in range(form.access_slots.data):
            db.session.add(Slot(is_open=True, facility_id=new_facility.id))
        db.session.commit()
        return redirect(url_for('orgs.view', org_id=new_facility.org_id))
    return render_template('facilities/new.html', form=form)


@bp.route('/manage')
@login_required
def manage():
    return render_template('facilities/manage.html')


@bp.route('/<int:facility_id>')
@login_required
def view(facility_id):
    facility = Facility.query.get(facility_id)
    return render_template('facilities/view.html', facility=facility)


@bp.route('/<int:facility_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(facility_id):
    facility = Facility.query.get(facility_id)
    form = FacilityForm(obj=facility)
    if form.validate_on_submit():
        facility.name = form.name.data
        facility.notes = form.notes.data
        facility.org_id = form.org.data
        analyses = []
        for analysis in form.analyses.data:
            analyses.append(Analysis.query.get(analysis))
        facility._analyses = analyses
        if form.access_slots.data < len(facility.slots):
            if form.access_slots.data < len(facility.closed_slots):
                form.access_slots.errors.append(
                    f'{len(facility.closed_slots)} are currently active and cannot be removed.')
                return render_template('facilities/edit.html', form=form, facility_id=facility_id,
                                       min_slots=max(len(facility.closed_slots), 1))
            for i, slot in zip(range(form.access_slots.data), facility.open_slots):
                db.session.delete(slot)
        elif form.access_slots.data > len(facility.slots):
            for i in range(form.access_slots.data - len(facility.slots)):
                db.session.add(Slot(is_open=True, facility_id=facility.id))
        db.session.commit()
        return redirect(url_for('facs.view', facility_id=facility_id))
    return render_template('facilities/edit.html', form=form, facility_id=facility_id,
                                       min_slots=max(len(facility.closed_slots), 1))
