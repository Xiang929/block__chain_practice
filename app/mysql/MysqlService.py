import pymysql

class MysqlService:
    db = pymysql.connect("localhost", "root", "123456", "blockchain")
    cursor = db.cursor()

    def addUser(self,id,password,name,phone,role):
        #sql = """INSERT INTO blockchain (id, pass, role, phone, name) VALUES ("+id+","+password+","+name+","+phone+","+role+")"""
        sql = "INSERT INTO blockchain_tbl(id, pass, role, phone, name) \
               VALUES ('%s', '%s', '%s', '%s', '%s' )" % \
              (id,password,name,phone,role)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
