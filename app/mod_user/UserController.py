from flask import  request,render_template
import json
from app.mod_user.User import User
from app.mysql.MysqlService import MysqlService
from app import app


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    # data = request.get_data()
    # data = str(data, encoding="utf8")
    # j_data = json.loads(data)

    id = request.form['userid']
    name = request.form['username']
    password = request.form['password']
    phone = request.form['userphone']
    role = request.form['userrole']
    user = User(id,password,name,phone,role)
    # add this  user to database
    mysql=MysqlService()
    mysql.addUser(id,password,name,phone,role)
    return '200'

@app.route('/user/login',methods=['POST','GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')

    data = request.get_data()
    data = str(data, encoding="utf8")
    j_data = json.loads(data)
    id = j_data['id']
    password = j_data['password']
    # get the password from database
    mysql = MysqlService()
    rea_pass = mysql.getPassById(id)
    print('realpass is'+str(rea_pass))
    if password == rea_pass:
        return '200'
    else:
        return 'pass error'

@app.route('/user/getGoods',methods=['GET''POST'])
def getGood():
    data = request.get_data()
    data = str(data, encoding="utf8")
    j_data = json.loads(data)
    if request.method=='POST':
        id = j_data['id']
        print(id)
    else:
        print('get')
    #get his role
    #get info from the block by his role
    return '200'

@app.route('/users/addGoods',methods=['POST'])
def addGoods():
    '''
    get the info of goods and add it to the block
    :return:
    '''
    data = request.get_data()
    data = str(data, encoding="utf8")
    j_data = json.loads(data)
    product_id = j_data['product_id']
    product_name=j_data['product_name']
    address=j_data['address']
    data=j_data['data']
    discription=j_data['discription']
    state=j_data['state']
    # add the goods to the blockchain
    return '200'


