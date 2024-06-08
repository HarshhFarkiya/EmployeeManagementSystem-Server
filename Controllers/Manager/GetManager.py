from ConnectSql import connect, disconnect
from Views.Manager import Manager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
def get_manager(id):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Query to find all the details of a employee
        cursor_object.execute(f"SELECT * FROM managers_information WHERE id='{id}'")
        result = cursor_object.fetchall()
        all_managers = Manager.get_manager_response(result)
        connection.commit()
        return JSONResponse(content={'message': 'Manager Details Fetched Successfully', 'result': all_managers},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)