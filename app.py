from flask import Flask, request, render_template, url_for
from flask.globals import current_app
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm, form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_bootstrap import Bootstrap


app = Flask(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)

#Hacemos una llave secreta con una cadena para que lo que se envie entre el servidor y el cliente se encripte
app.config['SECRET_KEY'] = 'hard to guess string'

# Clases para formularios

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
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('askName.html', form=form, name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorHandlers/404.html'), 404

@app.errorhandler(500)
def interenal_server_error(e):
    return render_template('errorHandlers/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
