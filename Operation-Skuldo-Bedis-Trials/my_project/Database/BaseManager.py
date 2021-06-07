import sqlite3 
from sqlite3 import Error
import os
class Base() :

    def __init__(self) :
        self.basepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"visiteur.db") 
        self.conn = None


    def connect(self) :
        try:
            self.conn = sqlite3.connect(self.basepath)
        except Error as e:
            print(e)



    def close(self) : 
          self.conn.close()


    def selectAll(self,number= -1,date='',columns='*',operator='=') :

        try :
            if number == -1 and date == '' :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur ;'''.format(columns))
                results = curso.fetchall()
                curso.close()
                return results
            elif number == -1 and date != '' and operator=='>' :
                curso = self.conn.cursor()
                
                curso.execute('Select {} from visiteur where DATE(date_) > DATE("{}");'.format(columns,date))
                results = curso.fetchall()
                curso.close()
                return results
            elif number == -1 and date != '' and operator=='=' :
                curso = self.conn.cursor()
                curso.execute('Select {} from visiteur where DATE(date_) = DATE("{}");'.format(columns,date))
                results = curso.fetchall()
                curso.close()
                return results
            elif number != -1 and date == '' :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur ;'''.format(columns))
                results = curso.fetchmany(number)
                curso.close()
                return results
            else :
                curso = self.conn.cursor()
                curso.execute('Select {} from visiteur where date_ > "{}";'.format(columns,date))
                results = curso.fetchmany(number)
                curso.close()
                return results
        except Error as e :
            print(e)
   

    def selectUnknows(self,number= -1,date='',columns = '*',operation='=') :
        try :
            if number == -1 and date == '' :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person='unknown' ;'''.format(columns))
                results = curso.fetchall()
                curso.close()
                return results
            elif number == -1 and date != '' and operation=='>' :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person='unknown' and DATE(date_) > DATE("{}");'''.format(columns,date))
                results = curso.fetchall()
                curso.close()
                return results
            elif number == -1 and date != '' and operation=='=' :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person='unknown' and DATE(date_) = DATE("{}");'''.format(columns,date))
                results = curso.fetchall()
                curso.close()
                return results
            elif number != -1 and date == '' :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person='unknown' ;'''.format(columns))
                results = curso.fetchmany(number)
                curso.close()
                return results
            else :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person='unknown' and date_ > "{}" ;'''.format(columns,date))
                results = curso.fetchmany(number)
                curso.close()
                return results
        except Error as e :
            print(e)


    def selectVerified(self,number= -1,date='',columns='*' ,operation='=') :
        try :
            if number == -1 and date == '' :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person <> 'unknown' ;'''.format(columns))
                results = curso.fetchall()
                curso.close()
                return results
            elif number == -1 and date != '' and operation=='>':
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person <>'unknown' and DATE(date_) > DATE("{}");'''.format(columns,date))
                results = curso.fetchall()
                curso.close()
                return results
            elif number == -1 and date != '' and operation=='=':
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person <>'unknown' and DATE(date_) = DATE("{}");'''.format(columns,date))
                results = curso.fetchall()
                curso.close()
                return results
            elif number != -1 and date == '' :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person <> 'unknown' ;'''.format(columns))
                results = curso.fetchmany(number)
                curso.close()
                return results
            else :
                curso = self.conn.cursor()
                curso.execute('''Select {} from visiteur where person <> 'unknown' and date_ > "{}" ;'''.format(columns,date))
                results = curso.fetchmany(number)
                curso.close()
                return results
        except Error as e :
            print(e)

    def insert(self,id,person = 'unknown') :
        with self.conn :
            self.conn.execute('''Insert into visiteur('ID','person') values(?,?)''',(id,person))
            self.conn.execute('''commit''')

    def update(self,id,name) :
        with self.conn :
            self.conn.execute('''update visiteur set person = ? where id = ? ''',(name,id))
            self.conn.execute('''commit''')



    def deleteAll(self) :
        with self.conn :
                self.conn.execute('''delete from visiteur ; ''')



    def createTable(self) :
        self.conn.execute('''CREATE TABLE visiteur
            (ID varchar2(20) Primary key     ,
            date_           Text    DEFAULT    (datetime('now','localtime')),
            person            varchar(50)     
            );''')
        

    def drop(self) :
        self.conn.execute("drop table visiteur ;")
base=Base()
base.connect()
print(base.selectAll())
base.close()
"""
base.close()
base.connect()
base.drop()
base.createTable()
base.insert('image1')
base.insert('image2','ahmed')
base.conn.execute('''Insert into visiteur('ID','date_','person') values('image3','2021-05-29 15:00:00','sami');''')
res = base.selectAll()
print(res)
res = base.selectAll(columns='id,person',date="2021-05-31 10:00:18",operator='=')
print(res)
res = base.selectUnknows(columns='id,date_',date='2021-05-28 14:00:00')
print(res)
res = base.selectVerified(columns='id,date_',date='2021-05-28 14:00:00')
print(res)
base.close()
"""