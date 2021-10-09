import itertools
from datetime import datetime as dt, timedelta
from datetimerange import DateTimeRange

from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user

from ..extensions import db, login_manager
from ..utils import countries_cache
from ..forms import ApplicationForm
from ..models import Application, Analysis, Org, Facility, Slot, Offer, application_analyses, facility_analyses

bp = Blueprint('apps', __name__, url_prefix='/apply')


def check_access(application, org=None, facility=None):
    can_access = [current_user.id == application.user_id, current_user.is_admin]
    if org:
        can_access.append(org.can_edit)
    if facility:
        can_access.append(facility.can_edit)
    if any(can_access):
        return True

@bp.route('/', methods=['GET', 'POST'])
@login_required
def new():
    form = ApplicationForm(desired_location=current_user.country)
    if form.validate_on_submit():
        new_app = Application(user_id=current_user.id,
                              desired_location=form.desired_location.data,
                              date_from=form.date_from.data,
                              date_to=form.date_to.data,
                              able_to_travel=form.able_to_travel.data,
                              fund_own_travel=form.fund_own_travel.data,
                              about_request=form.about_request.data,
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
    if not check_access(application):
        return login_manager.unauthorized()
    return render_template('apply/view.html', application=application)


@bp.route('/<int:app_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(app_id):
    application = Application.query.get(app_id)
    if not check_access(application):
        return login_manager.unauthorized()
    form = ApplicationForm(obj=application)
    if form.validate_on_submit():
        update_info = dict(user_id=current_user.id,
                           desired_location=form.desired_location.data,
                           date_from=form.date_from.data,
                           date_to=form.date_to.data,
                           able_to_travel=form.able_to_travel.data,
                           fund_own_travel=form.fund_own_travel.data,
                           about_request=form.about_request.data,
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


@bp.route('/<int:app_id>/find_matches')
@login_required
def find_matches(app_id):
    application = Application.query.get(app_id)
    if not check_access(application):
        return login_manager.unauthorized()
    analysis_ids = [a.id for a in application.analyses]

    # narrow by location
    if application.able_to_travel and not application.fund_own_travel:
        org_query = Org.query.filter(Org.will_fund_travel).all()
    elif not application.able_to_travel:
        org_query = Org.query.filter(Org.country == application.desired_location).all()
    else:
        org_query = []
    facs_loc = [fac.id for org in org_query for fac in org.facilities]

    # narrow by analysis
    fac_query = db.session.query(application_analyses) \
        .filter_by(application_id=app_id) \
        .join(facility_analyses, application_analyses.c.analysis_id == facility_analyses.c.analysis_id)
    if facs_loc:
        fac_query = fac_query.filter(facility_analyses.c.facility_id.in_(facs_loc))
    facs_analysis = fac_query.with_entities(facility_analyses.c.facility_id, facility_analyses.c.analysis_id).all()

    # narrow by slots - find anything that's occupied during the time range and ignore it
    slot_date_query = Slot.query.filter(Slot.facility_id.in_([f[0] for f in facs_analysis])).join(
        Offer)
    date_filters = []
    date_from = application.date_from or dt.now().date
    date_to = application.date_to or date_from + timedelta(years=5)
    date_range = DateTimeRange(date_from, date_to)
    date_filters.append(Offer.date_to >= date_from)
    date_filters.append(Offer.date_from <= date_to)
    slot_date_query = slot_date_query.filter(*date_filters).with_entities(Slot.id, Offer.date_from, Offer.date_to)
    slot_availability = {k: all([DateTimeRange(x[1], x[2]).is_intersection(date_range) for x in v]) for k, v in itertools.groupby(sorted(slot_date_query, key=lambda x: x[0]), key=lambda x: x[0])}
    filled_slots = [k for k, v in slot_availability.items() if v]
    fac_date_query = Facility.query.join(Slot).filter(Facility.id.in_([f[0] for f in facs_analysis]), Slot.id.not_in(filled_slots))
    facs_date = fac_date_query.all()

    matches = []
    for fac in facs_date:
        open_slots = Slot.query.filter(Slot.facility_id == fac.id, Slot.id.not_in(filled_slots)).all()
        sorted_slots = sorted(open_slots, key=lambda x: -len(x.gaps_in_range(date_from, date_to)))
        first_slot = sorted_slots[0]
        first_gap = first_slot.gaps_in_range(date_from, date_to)[0]

        match_dict = {
            'id': fac.id,
            'url': url_for('facs.view', facility_id=fac.id),
            'name': fac.name,
            'matching_analyses': [str(a) for a in fac.analyses if a.id in analysis_ids],
            'location': countries_cache[fac.org.country]['name'],
            'org_id': fac.org.id,
            'org_name': fac.org.name,
            'org_url': url_for('orgs.view', org_id=fac.org.id),
            'available': dt.strftime(first_gap[0], '%Y-%m-%d'),
            'until': dt.strftime(first_gap[1], '%Y-%m-%d'),
            'slot_id': first_slot.id,
            'travel_fund': fac.org.will_fund_travel
        }

        matches.append(match_dict)

    return jsonify(matches)


@bp.route('/make_match', methods=['POST'])
@login_required
def make_match():
    post_data = request.get_json()
    app_id = post_data['app_id']
    application = Application.query.get(app_id)
    slot_id = post_data['slot_id']
    slot = Slot.query.get(slot_id)
    facility = slot.facility
    if not check_access(application, facility=facility):
        return login_manager.unauthorized()
    date_from = post_data['date_from']
    date_to = post_data['date_to']
    try:
        new_offer = Offer(application_id=app_id, slot_id=slot_id, date_from=date_from, date_to=date_to)
        db.session.add(new_offer)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': e})

