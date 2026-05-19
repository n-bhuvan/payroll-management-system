import mysql.connector
try:
    connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="payroll_system"
    )
    if connection.is_connected():
        print("Connected Successfully")
except Exception as e:
    print("Error:",e)