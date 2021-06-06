from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World </h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello {}!</h1>'.format(name)

if __name__ == '__main__':
    app.run(debug=True)