import mysql.connector

def connect():
    # Connect to the database
    try:
        conn_obj = mysql.connector.connect(
        host="localhost",
        user="harsh",
        password="harsh123",
        database="NucleusTeq"  # Specify the database name here
    )
        return conn_obj
    except Exception as e:
        raise Exception("Internal Server Error",e)

def disconnect(conn_obj):
    # Disconnect from the database
    try:
        conn_obj.close()
    except Exception as e:
        raise Exception("Internal Server Error",e)