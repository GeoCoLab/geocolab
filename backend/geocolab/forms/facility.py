from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, TextAreaField

from ._fields import AnalysisField, OrgField


class FacilityForm(FlaskForm):
    name = StringField('Name')
    analysis = AnalysisField('Analysis type', validators=[validators.DataRequired()])
    access_slots = IntegerField('Available access slots', default=1)
    notes = TextAreaField('Further information')
    org = OrgField('Organisation/Institution', validators=[validators.DataRequired()])
