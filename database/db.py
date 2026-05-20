import mysql.connector

def connect_db():
    try:
        connection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="payroll_system"
        )
        if connection.is_connected():
            print("Connected Successfully")
            return connection 
    except Exception as e:
        print("Error:",e)

        return None
          