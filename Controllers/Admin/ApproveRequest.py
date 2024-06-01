from Models.Project.ProjectModel import Project;
from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json 
def approve_request(project):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Checking all the required parameters in request
        required_parameters = ['manager_id','project_id','resource_id']
        if not all(param in project for param in required_parameters):
            return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)

        
        #Check request Exists or not
        cursor_object.execute(f"SELECT * FROM resources_requested WHERE project_id=%s AND managers_id=%s AND resource_id=%s AND status=%s",(project['project_id'],project['manager_id'],project['resource_id'],0))
        check=len(cursor_object.fetchall())
        if check<=0:
            return JSONResponse(content={"message": "Request Doesnt Exists/Inactive"}, status_code=404)


        #To check wether the project exists or not
        cursor_object.execute(f"SELECT * FROM project_information WHERE project_id = '{project['project_id']}'")
        check = len(cursor_object.fetchall())
        if int(check) <= 0:
            return JSONResponse(content={"message": "Project Doesn't Exists, Please Provide a Valid Active Project Id"}, status_code=404)


        #To Check wether the employee/resoure id is valid or not
        cursor_object.execute(f"SELECT assigned FROM employees_information WHERE id = '{project['resource_id']}'")
        data=cursor_object.fetchall()
        check = len(data)
        if int(check) <= 0:
            return JSONResponse(content={"message": "Employee Doesn't Exists, Please Provide a Valid Employee Id"}, status_code=404)

        #Check wether employee is already assigned or not
        check = data[0][0]
        if int(check) ==1:
            return JSONResponse(content={"message": "Employee Already Assgined"}, status_code=200)


        #Check wether manager exists or not for the project            
        cursor_object.execute(f"SELECT employees_id FROM project_assigned WHERE project_id = '{project['project_id']}' AND managers_id IS NOT NULL")
        data=cursor_object.fetchall()
        check = len(data)
        if int(check) <= 0:
            return JSONResponse(content={"message": "Unable To Assigned Employee, Manager Doesn't Exists"}, status_code=404)

        #Check All the previous employees of project and add new employee in the list                
        prev_employees_result = data[0]
        if prev_employees_result is not None:
            prev_employees = prev_employees_result[0]
            if prev_employees:
                prev_employees = json.loads(prev_employees)
            else:
                prev_employees = []
        else:
            prev_employees = []
        prev_employees.append(project['resource_id'])
        new_employees_json = json.dumps(prev_employees)

        #Updating the new employees list in the project_assigned table
        cursor_object.execute(f"UPDATE project_assigned SET employees_id = %s WHERE project_id = %s", (new_employees_json, project['project_id']))


        #Updating the employee_informatio table for the assigned employee
        cursor_object.execute(f"UPDATE employees_information SET project_assigned = '{project['project_id']}',assigned = 1 WHERE id = '{project['resource_id']}'")

        #Updating the resources_requested table for the status of request
        cursor_object.execute(f"UPDATE resources_requested SET status=1 WHERE project_id=%s AND managers_id = %s AND resource_id=%s",(project['project_id'],project['manager_id'],project['resource_id']))
        connection.commit()
        return JSONResponse(content={"message": "Request Approved"}, status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally :
        disconnect(connection)
