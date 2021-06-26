from flask import render_template, redirect, url_for
from flask.globals import request
from flask.helpers import flash
from flask_login.utils import login_required, login_user, logout_user
from wtforms import form
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register')
def register():
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)