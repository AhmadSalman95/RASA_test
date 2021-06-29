import cx_Oracle
import logging

try:
    connection = cx_Oracle.connect(
        user="CHAT_BOOT",
        password="CHAT_BOOT",
        dsn="ereg-scan.psau.edu.sa:1521/ereg")
    logging.info("Successfully connected to Oracle Database")

except:
    logging.error("the DATABASE connection faild ...")

def checkEmail(user_email):
    try:
        cursor = connection.cursor()
    except:
        try:
            connection = cx_Oracle.connect(
                user="CHAT_BOOT",
                password="CHAT_BOOT",
                dsn="ereg-scan.psau.edu.sa:1521/ereg")
            logging.info("Successfully connected to Oracle Database")
            cursor = connection.cursor()

        except:
            logging.error("the DATABASE connection faild ...")
    insert_statment = """SELECT WORK_EMAIL
                         FROM EMPLOYEES
                         where WORK_EMAIL=:a """
        
    
    try:
        cursor.execute(insert_statment,{'a':user_email})
        result = cursor.fetchall()
        print(result)
        if (len(result)==1):
            return True
        else:
            return False
    except:
        logging.error("the DATA BASE Statment faild ....")
    finally:
        cursor.close()
        connection.close()
        logging.info("connection close")



# check=checkEmail('m.ibrahim@psau.edu.sa')
# print(check)