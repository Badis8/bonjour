import sqlite3 
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

basepath = r"E:\PROGRAMATION\Python\Operation Skuld\Database\visiteurs.db"
conn = create_connection(basepath)

try :
    curso = conn.cursor()


    curso.execute('''CREATE TABLE visiteur
          (ID varchar2(20)     ,
         date_           date    DEFAULT    (datetime('now','localtime')),
         path            varchar(50)     
         );''')
except Error as e :
    print(e)



print ("Table created successfully");

conn.execute('''Insert into visiteur('ID','path') values('image1','AaAa');

''')

try :
    curso = conn.cursor()
    curso.execute(''' Select * from visiteur      ;  ''')
except Error as e :
    print(e)



results  = curso.fetchall()
for i in results :
    print(i)


curso.close()
conn.close()