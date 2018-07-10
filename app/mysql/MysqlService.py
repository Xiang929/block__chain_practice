import pymysql

class MysqlService:
    db = pymysql.connect("localhost", "root", "wzp980402", "blockchain")
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

    def getPassById(self,id):
        sql = "SELECT pass from blockchain_tbl where id ='%s'"% (id)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            #print(results)
            for row in results:
                password = row[0]
                print(password)
                return password
        except:
            self.db.rollback()

    def deleteUser(self,id):
        sql = "DELETE from blockchain_tbl where id = '%s'"% (id)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def UpdateMessage(self,id,password):
        sql = "UPDATE blockchain_tbl SET id='%s' where pass='%s'"%(id,password)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()





