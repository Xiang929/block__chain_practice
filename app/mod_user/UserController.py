from flask import Flask, request
import json
from app.mod_user.User import User
from app.mysql.MysqlService import MysqlService
from app import app

@app.route('/user/register',methods=['POST'])
def register():
    data = request.get_data()
    data = str(data, encoding="utf8")
    j_data = json.loads(data)
    id = j_data['id']
    name = j_data['name']
    password = j_data['password']
    phone = j_data['phone']
    role = j_data['role']
    user = User(id,password,name,phone,role)
    # add this  user to database
    mysql=MysqlService()
    mysql.addUser(id,password,name,phone,role)
    return '200'

@app.route('/user/login',methods=['POST'])
def login():
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
    return 200


