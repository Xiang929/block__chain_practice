from app import app
from flask import request,render_template
from app.mod_qrcode.qrcode import QrCode

@app.route('/qrcode',methods=['POST','GET'])
def qrcode():
    print(request.get_data())
    #product_id = request.form['product_id']
    product_id='123'
    data={
        'product_id':product_id
    }
    path='app/static/images/'+product_id+'.jpg'
    QrCode().simpleQRMake(data,path)
    return render_template('showqrcode.html',path=product_id+'.jpg')