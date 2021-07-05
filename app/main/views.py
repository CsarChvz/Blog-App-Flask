from logging import error
from operator import pos
import re
from flask import render_template, session, redirect, url_for, current_app
from flask.globals import request
from flask.helpers import flash
from .. import db
from ..models import Permission, Post, User
from ..email import send_email
from . import main
from .forms import NameForm, EditProfile, PostForm
from datetime import datetime
from flask_login.utils import login_required, login_user, logout_user, current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)

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

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('404.html'), 404)
    posts = user.posts.all()
    return render_template('profile.html', posts=posts, user=user)


@main.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    user = current_user.username
    #print(user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        #db.session.add(current_user.__get_current_object())
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])