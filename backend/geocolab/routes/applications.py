import itertools
from datetime import datetime as dt, timedelta

from datetimerange import DateTimeRange
from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user

from ..extensions import db, login_manager
from ..forms import ApplicationForm
from ..models import Application, Analysis, Org, Facility, Slot, Offer, application_analyses, facility_analyses, info
from ..utils import countries_cache

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
                              about_request=form.about_request.data,
                              restrictions=form.restrictions.data,
                              current_org=form.current_org.data,
                              additional_requirements=form.additional_requirements.data,
                              days_estimate=form.days_estimate.data,
                              samples_estimate=form.samples_estimate.data,
                              about_you=form.about_you.data,
                              other_analyses=form.other_analyses.data,
                              access_type=form.access_type.data,
                              funding_level=form.funding_level.data)
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
                           about_request=form.about_request.data,
                           restrictions=form.restrictions.data,
                           current_org=form.current_org.data,
                           additional_requirements=form.additional_requirements.data,
                           days_estimate=form.days_estimate.data,
                           samples_estimate=form.samples_estimate.data,
                           about_you=form.about_you.data,
                           other_analyses=form.other_analyses.data,
                           access_type=form.access_type.data,
                           funding_level=form.funding_level.data)
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
    failed = []

    # narrow by org
    org_filters = []
    if application.access_type != 'any':
        org_filters.append(Org.accepted_access_types == application.access_type)
    if application.funding_required:
        domestic = Org.country == application.desired_location
        international = Org.country != application.desired_location
        if application.funding_level == 'none':
            org_filters.append(
                db.or_(db.and_(domestic, Org.funding_level != 'none'),
                       db.and_(international, Org.funding_level == 'international')))
        elif application.funding_level == 'domestic':
            org_filters.append(
                db.or_(domestic, db.and_(international, Org.funding_level == 'international'))
            )

    if org_filters:
        org_query = Org.query.filter(*org_filters).all()
    else:
        org_query = []
    facs_loc = [fac.id for org in org_query for fac in org.facilities]
    if not facs_loc:
        failed.append('No organisations with appropriate funding found.')

    # narrow by analysis
    fac_query = db.session.query(application_analyses) \
        .filter_by(application_id=app_id) \
        .join(facility_analyses, application_analyses.c.analysis_id == facility_analyses.c.analysis_id)
    if org_query:
        fac_query = fac_query.filter(facility_analyses.c.facility_id.in_(facs_loc))
    facs_analysis = fac_query.with_entities(facility_analyses.c.facility_id, facility_analyses.c.analysis_id).all()
    if not facs_analysis:
        failed.append('No facilities with required analyses found.')

    # narrow by slots - find anything that's occupied during the time range and ignore it
    slot_date_query = Slot.query.filter(Slot.facility_id.in_([f[0] for f in facs_analysis])).join(
        Offer)
    date_filters = []
    date_from = application.date_from or dt.now().date
    date_to = application.date_to or date_from + timedelta(days=365)
    date_range = DateTimeRange(date_from, date_to)
    date_filters.append(Offer.date_to >= date_from)
    date_filters.append(Offer.date_from <= date_to)
    slot_date_query = slot_date_query.filter(*date_filters).with_entities(Slot.id, Offer.date_from, Offer.date_to)
    slot_availability = {k: all([DateTimeRange(x[1], x[2]).is_intersection(date_range) for x in v]) for k, v in
                         itertools.groupby(sorted(slot_date_query, key=lambda x: x[0]), key=lambda x: x[0])}
    filled_slots = [k for k, v in slot_availability.items() if v]
    fac_date_query = Facility.query.join(Slot).filter(Facility.id.in_([f[0] for f in facs_analysis]))
    if filled_slots:
        fac_date_query = fac_date_query.filter(Slot.id.not_in(filled_slots))
    facs_date = fac_date_query.all()
    if not facs_date:
        failed.append('No open slots found.')

    matches = []
    for fac in facs_date:
        open_slots = Slot.query.filter(Slot.facility_id == fac.id, Slot.id.not_in(filled_slots)).all()
        slot_gaps = [(s, s.gaps_in_range(date_from, date_to, min_length=application.days_estimate or 1)) for s in
                     open_slots]
        sorted_slots = sorted(slot_gaps, key=lambda x: -x[1][0].days)
        first_slot = sorted_slots[0]
        first_gap = first_slot[1][0]

        match_dict = {
            'matching_analyses': [str(a) for a in fac.analyses if a.id in analysis_ids],
            'other_analyses': fac.other_analyses,
            'location': countries_cache[fac.org.country]['name'],
            'available': dt.strftime(first_gap.start, '%Y-%m-%d'),
            'until': dt.strftime(first_gap.start + timedelta(days=application.days_estimate or 1), '%Y-%m-%d'),
            'slot_id': first_slot[0].id,
            'funding_level': info.funding_level[fac.org.funding_level],
            'access_types': info.access_type[fac.org.accepted_access_types]
        }

        matches.append(match_dict)

    if matches:
        return jsonify({
            'success': True,
            'matches': matches,
            'count': len(matches)
        })
    else:
        return jsonify({
            'success': False,
            'errors': failed
        })


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
