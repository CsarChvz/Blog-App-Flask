from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField('Cuál es tu nombre?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfile(FlaskForm):
    name = StringField('Nombre Real', validators=[Length(0, 64)])
    location = StringField('Lugar', validators=[Length(0, 64)])
    about_me = TextAreaField('Acerca de mi')
    submite = SubmitField('Enter')

class PostForm(FlaskForm):
    body = TextAreaField("¿Qué tienes en tu mente?", validators=[DataRequired()])
    submit = SubmitField('Submit')