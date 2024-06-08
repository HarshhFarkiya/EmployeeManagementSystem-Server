from ConnectSql import connect, disconnect
from Views.Admin import ResourceRequests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
def get_all_requests():
    #Creating connection object
    connection = connect()
    #Creating cursor object
    cursor_object = connection.cursor()
    try:
        #Fetching all the resources requests from the resources_requested table
        cursor_object.execute(f"SELECT * FROM resources_requested")
        requests = cursor_object.fetchall()


        #Passign the result in the ResourceRequest View 
        final_requests = ResourceRequests.get_all_requests(requests)

        
        #Return result
        return JSONResponse(content={'message': 'Requests Fetched Successfully', 'result': final_requests},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)
