from flask import render_template, redirect, url_for
from flask_login.utils import login_required
from . import auth
from .forms import LoginForm

@auth.route('/login')
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'