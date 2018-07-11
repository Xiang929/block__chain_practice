from flask import Flask
from app.mod_qrcode.qrcode import QrCode

app = Flask(__name__, static_url_path="/static")

app.config.from_object('config')


@app.route('/')
def hello_world():
    return render_template('login.html');


@app.route('/main')
def main():
    return render_template('main.html');

from app.mod_user.UserController import *
from app.mod_qrcode.QrcodeController import *
