#Rutas, este archivo se creo con Telescope
from flask import session, render_template, redirect,url_for, flash
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
