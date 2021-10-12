from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, DateField, BooleanField, IntegerField, SelectField

from ._fields import CountryField, AnalysisField
from ..models.info import access_type, funding_level

class ApplicationForm(FlaskForm):
    analyses = AnalysisField('Facilities requested', validators=[validators.DataRequired()])
    other_analyses = TextAreaField('Other analyses')
    desired_location = CountryField('Starting location')
    date_from = DateField('Available from')
    date_to = DateField('Available until')
    days_estimate = IntegerField('Estimated days required')
    samples_estimate = IntegerField('Number of samples to process')
    about_request = TextAreaField('About your request')
    about_you = TextAreaField('About you')
    restrictions = TextAreaField('Restrictions')
    current_org = StringField('Current institution')
    additional_requirements = TextAreaField('Additional requirements')
    access_type = SelectField('Access type', choices=access_type.items(), default='any')
    funding_level = SelectField('Current travel/transport funding', choices=funding_level.items(), default='none')
    is_submitted = BooleanField('Submit now', default=True)
    prep_required = BooleanField('Sample prep required', default=True)
