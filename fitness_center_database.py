import mysql.connector
from mysql.connector import Error
from time import sleep
 # i hope it wokes. i cant spell works lol 
 # u the sad part is you have to put in your information in 
 #EVERY TIME.... it runs:)
 #going to fix the soon

def get_db_connection_new():
    print ("This is an example of how to interact with the provided SQL file, which you can download from the GitHub repository.\n The file is named \n sql_data.sql.")
    sleep(3)
    DB_name = (input("First, we got to connect to your own database server\n Your server's name?:  "))
    USER = (input("now the username?: "))
    PASSWORD = (input("and password?:  "))
    HOST = (input("and a hostname?\n ues localhost for default:  "))
    """connect to the mySQL database and return the connection object"""
    #database connection parameters
    db_name = DB_name
    user = USER
    password = PASSWORD
    host = HOST

    try:
        #attempting to establish a connection
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        #chect if the connection is successful
        if conn.is_connected():
            print("connected to mysql database successfully")
            return conn
    
    except Error as e:
        #handling any connection errors
        print(f'error: {e}')
        return None
    

if __name__ == "__main__":
    connection = get_db_connection_new()
    if connection:
        # You can perform further operations here if needed
        connection.close()