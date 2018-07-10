from flask import render_template, Flask

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def index():
    return render_template('login.html');

from app.mod_user.UserController import *

