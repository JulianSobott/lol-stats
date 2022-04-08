from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/login/')
def login():
    return 'User logging in'


if __name__ == '__main__':
    app.run(debug=True)
