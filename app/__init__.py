from flask import  Flask,send_from_directory

app = Flask(__name__, static_url_path="/static")
app.config.from_object('config')

@app.route('/')
def log_():
    return render_template('login.html')


from app.mod_user.UserController import *
from app.mod_goods.GoodsController import *
from app.mod_qrcode.QrcodeController import *