from flask import Flask, request, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorHandlers/404.html'), 404

@app.errorhandler(500)
def interenal_server_error(e):
    return render_template('errorHandlers/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)