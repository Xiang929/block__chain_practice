import pymysql
from config import *


class MysqlService:
    db = pymysql.connect(MYSQL_URL, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE)
    cursor = db.cursor()

    def addUser(self, id, password, name, phone, role):
        # sql = """INSERT INTO blockchain (id, pass, role, phone, name) VALUES ("+id+","+password+","+name+",
        # "+phone+","+role+")"""
        sql = "INSERT INTO blockchain_tbl(id, pass, role, phone, name) \
               VALUES ('%s', '%s', '%s', '%s', '%s')" % \
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

    def UpdateMessage(self, name, phone,id):
        sql = "UPDATE blockchain_tbl SET name='%s',phone='%s' where id='%s'" % (name, phone,id)
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

    def addChainIdToUser(self,id,uuid):
        sql_chain = "SELECT chain from blockchain_tbl where id ='%s'" % (id)
        self.cursor.execute(sql_chain)
        results = self.cursor.fetchall()
        for row in results:
            preChainName = row[0]
        if preChainName!=None:
            chain_name=preChainName+' '+uuid
        else:
            chain_name=uuid
        sql_name = "UPDATE blockchain_tbl SET chain='%s' where id='%s'" % (chain_name, id)
        try:
            self.cursor.execute(sql_name)
            self.db.commit()
            print('Add the chain: '+uuid)
        except:
            print('Add chain failed')
            self.db.rollback()

    def getCanAddChainID(self,roleNum):
        if roleNum==1:
            RoleName='Meteria'
        if roleNum==2:
            RoleName='Product'
        if roleNum==3:
            RoleName='Transport'
        if roleNum==4:
            RoleName='Sale'

        # sql_chain = "SELECT role='%s', group_concat(chain separator ' ') from blockchain_tbl group by role" % (RoleName)
        sql_chain="SELECT chain from blockchain_tbl where role ='%s'" % (RoleName)
        print(sql_chain)
        self.cursor.execute(sql_chain)
        results = self.cursor.fetchall()

        pre=[]
        for row in results:
            if row[0] is not None:
                row = list(row)
                row_list = row[0].split()
                row_list = list(set(row_list))
                pre += row_list
        pre = list(set(pre))
        print(pre)
        chainName=pre
        return chainName

