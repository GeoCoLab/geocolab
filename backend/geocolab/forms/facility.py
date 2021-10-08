from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, TextAreaField, FormField, FieldList

from ._fields import AnalysisField, OrgField


class FacilityForm(FlaskForm):
    name = StringField('Name')
    analyses = AnalysisField()
    access_slots = IntegerField('Available access slots', default=1)
    notes = TextAreaField('Further information')
    org = OrgField('Organisation/Institution', validators=[validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        super(FacilityForm, self).__init__(*args, **kwargs)