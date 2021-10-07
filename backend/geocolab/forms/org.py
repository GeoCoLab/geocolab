from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, BooleanField
from ._fields import CountryField


class OrgForm(FlaskForm):
    ror_id = StringField('ROR ID')
    name = StringField('Name', validators=[validators.DataRequired()])
    country = CountryField('Location', validators=[validators.DataRequired()])
