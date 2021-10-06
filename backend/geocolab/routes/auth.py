from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user

from ..extensions import db, login_manager
from ..forms import LoginForm, RegisterForm
from ..models import User

bp = Blueprint('auth', __name__, url_prefix='/')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = []
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(email=email).one_or_none()

        if not user:
            errors.append('Email not found')
        elif not user.password_verify(password):
            errors.append('Incorrect password')
        else:
            login_user(user, remember=remember)
            return redirect(url_for('home.index'))
    return render_template('login.html', form=form, errors=errors)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    errors = []
    if form.validate_on_submit():
        email = form.email.data

        if User.query.filter_by(email=email).one_or_none():
            errors.append('A user with this email already exists.')
        else:
            new_user = User(email=email, name=form.name.data, country=form.country.data)
            new_user.password_set(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            return redirect(url_for('home.index'))
    return render_template('register.html', form=form, errors=errors)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))
