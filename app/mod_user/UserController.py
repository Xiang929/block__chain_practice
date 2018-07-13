from flask import request, render_template
import json
from app.mod_user.User import User
from app.mysql.MysqlService import MysqlService
from app import app


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



