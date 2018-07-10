from flask import Flask, render_template,request
from app.mod_user import User
app = Flask(__name__)

app.route('/user/register',methods=['POST'])
def register():
    id=request.form['id']
    name=request.form['name']
    password=request.form['password']
    phone=request.form['phone']
    role=request.form['role']
    user=User(id,name,password,phone,role)
    return user
    #add this  user to database

app.route('/user/login',methods=['POST'])
def login():
    id=request.form['id']
    password=request.form['password']

    #get the password from database
    rea_pass=''
    if password==rea_pass:
        return 200

app.route('/user/getGoods',methods=['GET'])
def getGood():
    id=request.form['id']
    #get his role
    #get info from the block by his role


app.route('/users/addGoods',methods=['POST'])
def addGoods():
    '''
    get the info of goods and add it to the block
    :return:
    '''
    return 200



