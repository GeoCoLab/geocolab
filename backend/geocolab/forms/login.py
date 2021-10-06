from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, BooleanField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember = BooleanField('Stay logged in', default=False)
