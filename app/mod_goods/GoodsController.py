from app import  app
from flask import render_template

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
    return render_template('userInfor.html')