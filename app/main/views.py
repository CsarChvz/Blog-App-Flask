from flask import render_template, session, redirect, url_for, current_app
from flask.helpers import flash
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm
from datetime import datetime
@main.route('/')
def index():
    return render_template('index.html',\
        current_time = datetime.utcnow())

@main.route('/user/<name>')
def user_name(name):
    return render_template('user.html', name=name)

@main.route('/askName', methods=['GET', 'POST'])
def askName():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name! ')
        session['name'] = form.name.data
        return redirect(url_for('.askName'))
    return render_template('askName.html', form=form, name = session.get('name'))
