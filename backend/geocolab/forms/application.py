from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, DateField, BooleanField

from ._fields import CountryField, AnalysisField


class ApplicationForm(FlaskForm):
    analyses = AnalysisField('Facilities requested', validators=[validators.DataRequired()])
    desired_location = CountryField('Starting location')
    date_from = DateField('Intended start date')
    date_to = DateField('Intended end date')
    about_request = TextAreaField('About your request')
    restrictions = TextAreaField('Restrictions')
    current_org = StringField('Current institution')
    additional_requirements = TextAreaField('Additional requirements')
    able_to_travel = BooleanField('Able to travel')
    fund_own_travel = BooleanField('Can self-fund travel')
    is_submitted = BooleanField('Submit now', default=True)
