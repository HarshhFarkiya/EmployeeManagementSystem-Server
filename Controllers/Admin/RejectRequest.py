from Models.Project.ProjectModel import Project;
from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json 
def reject_request(project):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Checking All the required parameters present in the request or not
        required_parameters = ['manager_id','project_id','resource_id']
        if not all(param in project for param in required_parameters):
            return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)
        
        #Check request Exists or not
        cursor_object.execute(f"SELECT * FROM resources_requested WHERE project_id=%s AND managers_id=%s AND resource_id=%s",(project['project_id'],project['manager_id'],project['resource_id']))
        check=len(cursor_object.fetchall())
        if check<=0:
            return JSONResponse(content={"message": "Request Doesnt Exists/Inactive"}, status_code=404)

        #Rejecting the request by setting the status -1
        cursor_object.execute(f"UPDATE resources_requested SET status=-1 WHERE project_id=%s AND managers_id=%s AND resource_id=%s",(project['project_id'],project['manager_id'],project['resource_id']))
        connection.commit()
        return JSONResponse(content={"message": "Request Rejected"}, status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally :
        disconnect(connection)
