from flask import  Flask,send_from_directory,session, redirect, url_for, escape, request,g


app = Flask(__name__, static_url_path="/static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config.from_object('config')

@app.route('/')
def log_():
    if 'userid' in session:
        return render_template('searchGoods.html')
    return render_template('login.html')

@app.before_request
def before_user():
    if 'userid' in session:
        print('userid is in session')
        g.userid=session.get('userid')
        print('g userid is '+g.userid)
    if 'role' in session:
        g.role = session.get('role')
        print('g role is '+g.role)

from app.mod_user.UserController import *
from app.mod_goods.GoodsController import *
from app.mod_qrcode.QrcodeController import *