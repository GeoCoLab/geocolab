from flask_wtf import FlaskForm
from wtforms import StringField, validators, BooleanField, IntegerField, SelectField

from ._fields import CountryField
from ..models.info import access_type, funding_level


class OrgForm(FlaskForm):
    ror_id = StringField('ROR ID')
    name = StringField('Name', validators=[validators.DataRequired()])
    country = CountryField('Location', validators=[validators.DataRequired()])
    accepted_access_types = SelectField('Accepted access type', choices=access_type.items(), default='any')
    funding_level = SelectField('Maximum travel/transport funding', choices=funding_level.items(), default='none')
    funding_limit = IntegerField('Expenses limit per applicant (GBP)')

