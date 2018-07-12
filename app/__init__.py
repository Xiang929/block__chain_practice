from flask import  Flask,send_from_directory

app = Flask(__name__, static_url_path="/static")

app.config.from_object('config')


@app.route('/')
def log_():
    return render_template('login.html')


@app.route('/searchGoods')
def search_goods():
    return render_template('searchGoods.html')


@app.route('/createGoods')
def create_goods():
    return render_template('createGoods.html')


from app.mod_user.UserController import *
