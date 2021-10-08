from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, DateField, BooleanField

from ._fields import CountryField, AnalysisField


class ApplicationForm(FlaskForm):
    analyses = AnalysisField('Facilities requested', validators=[validators.DataRequired()])
    current_location = CountryField('Desired location')
    date_from = DateField('Intended start date')
    date_to = DateField('Intended end date')
    reason_for_request = TextAreaField('About your request')
    restrictions = TextAreaField('Restrictions')
    current_org = StringField('Current institution')
    additional_requirements = TextAreaField('Additional requirements')
    is_submitted = BooleanField('Submit now', default=True)
