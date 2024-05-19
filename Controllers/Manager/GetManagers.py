from ConnectSql import connect, disconnect
from Views.Manager import Manager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
def get_all_managers():
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Query to find all the managers
        cursor_object.execute("SELECT * FROM managers_information")
        result = cursor_object.fetchall()
        all_managers = Manager.get_manager_response(result)
        connection.commit()
        return JSONResponse(content={'message': 'All managers Fetched Successfully', 'result': all_managers},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)
