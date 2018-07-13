from flask import request, render_template
import json
from app.mod_user.User import User
from app.mysql.MysqlService import MysqlService
from app import app
from app.mod_commodity.blockchain import Blockchain
from app.mod_publisher.subscriber import Subscriber
from config import *

subscriber = Subscriber(SERVER, PORT)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    id = request.form['userid']
    name = request.form['username']
    password = request.form['password']
    phone = request.form['userphone']
    role = request.form['userrole']
    user = User(id, password, name, phone, role)
    # add this  user to database
    mysql = MysqlService()
    mysql.addUser(id, password, name, phone, role)
    return render_template('login.html')


@app.route('/user/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    print(request.get_data())
    id = request.form['username']
    password = request.form['password']
    # get the password from database
    mysql = MysqlService()
    rea_pass = mysql.getPassById(id)
    if password == rea_pass:
        return render_template('searchGoods.html')
    else:
        return render_template('fail.html')


@app.route('/user/edit', methods=['GET', 'POST'])
def editUser(password, newpass):
    id = request.form['username']
    password = request.form['password']
    newpass = request.form['newpass']
    mysql = MysqlService()
    rea_pass = mysql.getPassById(id)
    if rea_pass == password:
        mysql.UpdateMessage(id, newpass)
    else:
        return 'error'


@app.route('/user/getGoods', methods=['GET', 'POST'])
def getGood():
    # data = request.get_data()
    # data = str(data, encoding="utf8")
    # j_data = json.loads(data)
    # if request.method=='POST':
    #     id = j_data['id']
    #     print(id)
    # else:
    #     print('get')

    # get his role
    # get info from the block by his role
    # blockchain = Blockchain()
    res = subscriber.blockchain.full_chain()
    return res


@app.route('/user/addGoods', methods=['POST'])
def addGoods():
    '''
    get the info of goods and add it to the block
    :return:
    '''
    product_id = request.form['product_id']
    product_name = request.form['product_name']
    address = request.form['address']
    data = request.form['date']
    discription = request.form['product_des']
    state = request.form['status']
    # add the goods to the blockchain
    dict = {'number': product_id, 'name': product_name, 'address': address, 'date': data, 'description': discription,
            'status': state}
    # block=Blockchain()
    subscriber.send_message('new block', dict)
    # if res is not None:
    #     return render_template('createGoods.html', res='success')
    # else:
    #     return render_template('createGoods.html', res='fail')
    return render_template('createGoods.html', res='success')
