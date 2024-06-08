from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import logging

def request_resource(request):
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Checking the required parameters exists in the request or not
        required_parameters = ['manager_id', 'project_id','resource_id']
        if not all(param in request for param in required_parameters):
            logging.error("Missing Parameters")
            return JSONResponse(content={'message': 'Missing required parameters'},status_code=422)
        id=request['manager_id']
        project_id=request['project_id']
        resource_id=request['resource_id']

        #Check the manager id is valid or not
        cursor_object.execute(f"SELECT * FROM managers_information WHERE id='{id}'")
        check = cursor_object.fetchall()
        if len(check)<=0 :
            logging.error("Invalid Manager Id")
            return JSONResponse(content={'message': 'Invalid manager id'},status_code=404)

        #Check the project id is valid or not
        cursor_object.execute(f"SELECT * FROM project_information WHERE project_id='{project_id}'")
        check=cursor_object.fetchall()
        if len(check)<=0:
            logging.error("Invalid Project Id")
            return JSONResponse(content={'message': 'Invalid project id'},status_code=404)

        #Check the resource id is valid or not
        cursor_object.execute(f"SELECT project_assigned FROM employees_information WHERE id='{resource_id}'")
        data=cursor_object.fetchall()
        if len(data)<=0:
            logging.error("Invalid Resource Id")
            return JSONResponse(content={'message': 'Invalid resource id'},status_code=404)
        #Check the employee is already assigned to the project
        check=data[0]
        if check[0] == project_id:
             return JSONResponse(content={'message': 'Resource Already Present'},status_code=200)
        #Check Wehter Manager is assigned to that project or not
        cursor_object.execute(f"SELECT managers_id FROM project_assigned WHERE project_id='{request['project_id']}'")
        prev_managers_result = cursor_object.fetchone()
        if prev_managers_result is not None:
            prev_managers = prev_managers_result[0]
            if prev_managers:
                prev_managers = json.loads(prev_managers)
            else:
                prev_managers = []
        else:
            prev_managers = []

        #if manager is not assigned to that project
        if request['manager_id'] not in prev_managers:
            logging.error("Request not allowed")
            return JSONResponse(content={'message': 'Unauthorized Assignment(Project not assinged)'},status_code=403)
        cursor_object.execute(f"SELECT status FROM resources_requested WHERE managers_id=%s AND resource_id=%s AND project_id=%s",(id,resource_id,project_id))
        check = cursor_object.fetchall()

        #Check the requests is already exists and active for that resource id and manager id
        if len(check)>=1:
            for req in check:
                if req[0]==0:
                    logging.info("Rquest Exists")
                    return JSONResponse(content={'message': 'Request Exists'},status_code=200)


        #If not then make a request 
        cursor_object.execute(f"INSERT INTO resources_requested VALUES(%s,%s,%s,%s)",(project_id,id,resource_id,0))
        connection.commit()
        logging.info("Resource Requested")
        return JSONResponse(content={'message': 'Resource Requested successfully'},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        logging.error(e)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)

