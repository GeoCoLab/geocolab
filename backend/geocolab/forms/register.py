from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, PasswordField
from ._fields import CountryField


required = [validators.DataRequired()]


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=required)
    password = PasswordField('Password', validators=required)
    name = StringField('Name', validators=required)
    country = CountryField('Country')
