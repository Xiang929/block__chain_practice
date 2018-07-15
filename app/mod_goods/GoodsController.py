from app import app
from flask import render_template, request, g, redirect, url_for
from app.mod_publisher.subscriber import Subscriber
from config import *
from app import MysqlService
import uuid

subscriber = Subscriber(SERVER, PORT)
new_flag = False


@app.route('/searchGoods')
def search_goods():
    if hasattr(g, 'userid'):
        print(g.userid)
        return render_template('searchGoods.html')
    return redirect(url_for('login'))


@app.route('/showGoods')
def show_goods():
    if hasattr(g, 'userid'):
        print(g.userid)
        return render_template('showGoods.html')
    return redirect(url_for('login'))


@app.route('/createGoods')
def create_goods():
    if hasattr(g, 'userid'):
        print(g.role)
        print(len(subscriber.block_chain.chain))
        if g.role=='Meteria':
            productID=generateUUID()
            return render_template('createGoods.html',type='M',block=productID,role=g.role)
        else:
            chainName=isCanAddGoods(g.role)
            return render_template('createGoods.html',type='O',block=chainName,role=g.role)

        # if (len(subscriber.block_chain.chain)==0 and g.role=="Meteria") or (len(subscriber.block_chain.chain) == 1 and g.role == "Product") or (len(subscriber.block_chain.chain) == 2 and g.role == "Transport") or (len(subscriber.block_chain.chain) == 3 and g.role == "Sale"):
        #     return render_template('createGoods.html',role=g.role, disabled="false")
        # else:
        #     return render_template('createGoods.html', role=g.role, disabled="true")
    return redirect(url_for('login'))


@app.route('/modifyGoods')
def modify_goods():
    if hasattr(g, 'userid'):
        return render_template('modifyGoods.html')
    return redirect(url_for('login'))


@app.route('/userInfor')
def userInfor():
    if hasattr(g, 'userid'):
        mysql = MysqlService()
        userIn = mysql.getUserInforByID(g.userid)
        print(userIn)
        return render_template('userInfor.html', userid=g.userid, username=userIn[0], userphone=userIn[1],
                               userrole=userIn[2])
    return redirect(url_for('login'))


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
    res = subscriber.block_chain.full_chain()
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
    mysql = MysqlService()
    mysql.addChainIdToUser(g.userid, product_id)
    subscriber.send_message('new block', dict)
    while new_flag is False:
        pass


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
    index = 2
    # add the goods to the blockchain
    dict = {'index': index, 'number': product_id, 'name': product_name, 'address': address, 'date': data,
            'description': discription,
            'status': state}
    # block=Blockchain()
    # subscriber.send_message('modify block', dict)
    result = subscriber.blockchain.modify_block(dict)
    if result == None:
        return render_template('modifyGoods.html', res='fail')
    # if res is not None:
    #     return render_template('createGoods.html', res='success')
    # else:
    #     return render_template('createGoods.html', res='fail')
    return render_template('modifyGoods.html', res='success')







def isCanAddGoods(currentRole):
    mysql=MysqlService()

    currentNum=changeRoleToNum(currentRole)

    if (currentNum==2 or currentNum==4):
        canAddChainID=mysql.getCanAddChainID(currentNum-1)
        print(canAddChainID)
        return canAddChainID

    if currentNum==3:
        canAddChainID = mysql.getCanAddChainID(currentNum - 1)
        print(canAddChainID)
        return canAddChainID


def changeRoleToNum(role):
    if role=='Meteria':
        return 1
    if role=='Product':
        return 2
    if role=='Transport':
        return 3
    if role=='Sale':
        return 4

def generateUUID():
    productid_uu=uuid.uuid1()
    productid_uu_str=str(productid_uu)
    productid=productid_uu_str[0:8]
    print('Generate the product id: '+productid)
    return productid