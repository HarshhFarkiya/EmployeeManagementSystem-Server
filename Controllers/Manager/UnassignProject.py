from ConnectSql import connect, disconnect
import json 
from fastapi import FastAPI
from fastapi.responses import JSONResponse
def unassign_project_manager(manager):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Check required parameters exists in the request or not
        required_parameters = ['manager_id','project_id']
        if not all(param in manager for param in required_parameters):
            return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)

        #Check Manager exists or not
        cursor_object.execute(f"SELECT * FROM managers_information WHERE id = '{manager['manager_id']}'")
        check = len(cursor_object.fetchall())
        if int(check) <= 0:
            return JSONResponse(content={"message":"Invalid Manager Id"},status_code=404)
        project_id = manager['project_id']

        #Check Project exists or not
        cursor_object.execute(f"SELECT * FROM project_information WHERE project_id = '{project_id}'")
        check = len(cursor_object.fetchall())
        if int(check) <= 0:
            return JSONResponse(content={"message":"Invalid Project Id"},status_code=404)

        
        #Fetching all the managers of given project id and remove the requested manager from the list
        cursor_object.execute(f"SELECT managers_id FROM project_assigned WHERE project_id='{project_id}'")
        prev_managers_result = cursor_object.fetchone()
        if prev_managers_result is not None:
            prev_managers = prev_managers_result[0]
            if prev_managers:
                prev_managers = json.loads(prev_managers)
            else:
                prev_managers = []
        else:
            prev_managers = []
        if manager['manager_id'] in prev_managers:
            prev_managers.remove(manager['manager_id'])
        new_managers_json = json.dumps(prev_managers)
        if len(prev_managers)==0:
            new_managers_json=None            
        #Updating the managers information to project_assigned table
        cursor_object.execute(f"UPDATE project_assigned SET managers_id = %s WHERE project_id = %s", (new_managers_json, project_id))

        #Updating the manager_information table, removing the given project id from the assigned projects to manager
        cursor_object.execute(f"SELECT projects_assigned FROM managers_information WHERE id='{manager['manager_id']}'")
        prev_projects_result = cursor_object.fetchone()
        if prev_projects_result is not None:
            prev_projects = prev_projects_result[0]
            if prev_projects:
                prev_projects = json.loads(prev_projects)
            else:
                prev_projects = []
        else:
            prev_projects = []
        if project_id in prev_projects:
            prev_projects.remove(project_id)
        else :
            return JSONResponse(content={"message":"Project Id Doesn't Exists For the manager, Please Provide a Valid Project Id"},status_code=404)
        new_projects_json = json.dumps(prev_projects)
        if len(prev_projects)==0:
            new_projects_json=None
        cursor_object.execute(f"UPDATE managers_information SET projects_assigned = %s WHERE id = %s", (new_projects_json, manager['manager_id']))
        connection.commit()
        return JSONResponse(content={'message': 'Manager is Unssigned from project successfully'},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally :
        disconnect(connection)
