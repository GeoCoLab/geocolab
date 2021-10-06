from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, PasswordField
from ..utils import countries


required = [validators.DataRequired()]


class RegisterForm(FlaskForm):
    email = StringField('email', validators=required)
    password = PasswordField('password', validators=required)
    name = StringField('name', validators=required)
    country = SelectField('country', choices=sorted([(c['iso3'], c['name']) for c in countries], key=lambda x: x[1]))
