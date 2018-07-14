import pymysql
from config import *


class MysqlService:
    db = pymysql.connect(MYSQL_URL, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE)
    cursor = db.cursor()

    def addUser(self, id, password, name, phone, role):
        # sql = """INSERT INTO blockchain (id, pass, role, phone, name) VALUES ("+id+","+password+","+name+",
        # "+phone+","+role+")"""
        sql = "INSERT INTO blockchain_tbl(id, pass, role, phone, name) \
               VALUES ('%s', '%s', '%s', '%s', '%s' )" % \
              (id, password, role, phone, name)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def getPassById(self, id):
        sql = "SELECT pass from blockchain_tbl where id ='%s'" % (id)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                password = row[0]
                return password
        except:
            self.db.rollback()

    def deleteUser(self, id):
        sql = "DELETE from blockchain_tbl where id = '%s'" % (id)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def UpdateMessage(self, id, password):
        sql = "UPDATE blockchain_tbl SET id='%s' where pass='%s'" % (id, password)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def getUserInforByID(self,id):
        sql_name = "SELECT name from blockchain_tbl where id ='%s'" % (id)
        sql_phone = "SELECT phone from blockchain_tbl where id ='%s'" % (id)
        sql_role = "SELECT role from blockchain_tbl where id ='%s'" % (id)
        try:
            self.cursor.execute(sql_name)
            results = self.cursor.fetchall()
            for row in results:
                name = row[0]
            self.cursor.execute(sql_phone)
            results = self.cursor.fetchall()
            for row in results:
                phone=row[0]
            self.cursor.execute(sql_role)
            results = self.cursor.fetchall()
            for row in results:
                role = row[0]
            return [name,phone,role]
        except:
            self.db.rollback()