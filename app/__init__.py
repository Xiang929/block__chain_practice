from flask import  Flask,send_from_directory

app = Flask(__name__, static_url_path="/static")

app.config.from_object('config')
@app.route('/')
def hello_world():
    return render_template('login.html');

from app.mod_user.UserController import *

