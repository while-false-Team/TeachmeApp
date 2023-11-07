import mysql.connector
import global_variables

try: 
    global_variables.mydb=mysql.connector.connect(
        host='195.164.130.186',
        user='agielski',
        password='iqafL4Z8exHLJ43',
        port='3306',
        database='angielski'
    )
    global_variables.mycursor=global_variables.mydb.cursor()
    global_variables.is_connected = True
except:
    is_connected = False

def tryAgain():
    global global_variables
    try:     
        global_variables.mydb=mysql.connector.connect(
            host='195.164.130.186',
            user='agielski',
            password='iqafL4Z8exHLJ43',
            port='3306',
            database='angielski'
        )
        global_variables.mycursor=global_variables.mydb.cursor()
        return True
    except:
        return False
