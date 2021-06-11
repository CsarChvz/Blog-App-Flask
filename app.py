from flask import Flask, request, render_template, url_for, redirect, flash
from flask.globals import current_app, session
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm, form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_bootstrap import Bootstrap
import os 
from flask-sqlalchemy import SQLAlchemy


app = Flask(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)

#Hacemos una llave secreta con una cadena para que lo que se envie entre el servidor y el cliente se encripte
app.config['SECRET_KEY'] = 'hard to guess string'
#Configuracion para la base de datos
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///file.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# Clases para formularios


db = SQLAlchemy(app)

#Modelos para base de datos

class Role(db.Model):

    __table__name = 'roles'
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(64), unique=True)

    def __repr__(self) -> str:
        return '<Role %r>' % self.name

class NameForm(FlaskForm):
    # Se hace un objeto con los clases
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html',\
        current_time = datetime.utcnow())

@app.route('/user/<name>')
def user_name(name):
    return render_template('user.html', name=name)

@app.route('/askName', methods=['GET', 'POST'])
def askName():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name! ')
        session['name'] = form.name.data
        return redirect(url_for('askName'))
    return render_template('askName.html', form=form, name = session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorHandlers/404.html'), 404

@app.errorhandler(500)
def interenal_server_error(e):
    return render_template('errorHandlers/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
