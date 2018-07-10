from flask import  Flask,send_from_directory

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def index():
    return render_template('login.html');

# @app.route('/register',methods=['POST','GET'])
# def register():
#     if request.method == 'GET':
#         return render_template("register.html")
#     # data = request.get_data()
#     # data = str(data, encoding="utf8")
#     # j_data = json.loads(data)
#
#     id = request.form['userid']
#     name = request.form['username']
#     password = request.form['password']
#     phone = request.form['userphone']
#     role = request.form['userrole']
#     user = User(id,password,name,phone,role)
#     # add this  user to database
#     mysql=MysqlService()
#     mysql.addUser(id,password,name,phone,role)
#     return '200'
@app.route('/plugins/<path:path>')
def egt(path):
    print('sa')
    return send_from_directory('static/plugins/jquery.validate',path)


from app.mod_user.UserController import *

from static import *
