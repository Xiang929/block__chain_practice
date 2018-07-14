from app import app
from flask import render_template,request
from app.mod_publisher.subscriber import Subscriber
from config import *

subscriber = Subscriber(SERVER, PORT)

@app.route('/searchGoods')
def search_goods():
    return render_template('searchGoods.html')


@app.route('/createGoods')
def create_goods():
    return render_template('createGoods.html')

@app.route('/modifyGoods')
def modify_goods():
    return render_template('modifyGoods.html')

@app.route('/userInfor')
def userInfor():
    return render_template('userInfor.html',userid='id',username='Jaye',userphone='11111',userrole='生产商')


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


@app.route('/user/editGoods', methods=['POST'])
def editGoods():
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
    index=2
    # add the goods to the blockchain
    dict = {'index':index ,'number': product_id, 'name': product_name, 'address': address, 'date': data, 'description': discription,
            'status': state}
    # block=Blockchain()
    #subscriber.send_message('modify block', dict)
    result=subscriber.blockchain.modify_block(dict)
    if result == None:
        return render_template('modifyGoods.html', res='fail')
    # if res is not None:
    #     return render_template('createGoods.html', res='success')
    # else:
    #     return render_template('createGoods.html', res='fail')
    return render_template('modifyGoods.html', res='success')