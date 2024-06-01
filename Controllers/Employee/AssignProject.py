from Models.Project.ProjectModel import Project;
from ConnectSql import connect, disconnect
import json 
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

def assign_project_employee(project):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Checking all the required parameters are present or not in the request
        required_parameters = ['employee_id','project_id']
        if not all(param in project for param in required_parameters):
            logging.error("Missing Parameters")
            return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)

        
        #To check wether the project exists or not
        cursor_object.execute(f"SELECT * FROM project_information WHERE project_id = '{project['project_id']}'")
        check = len(cursor_object.fetchall())
        if int(check) <= 0:
            logging.error("Project Doesn't Exists")
            return JSONResponse(content={"message":"Project Doesn't Exists, Please Provide a Valid Active Project Id"},status_code=404)

        
        #To check wether the employee exists or not and assigned or not
        cursor_object.execute(f"SELECT assigned FROM employees_information WHERE id='{project['employee_id']}'")
        data = cursor_object.fetchall()
        check = len(data)
        if int(check) <= 0:
            logging.error("Employee Doesn't Exists")
            return JSONResponse(content={"message":"Employee Doesn't Exists, Please Provide a Valid Employee Id"},status_code=404)
        elif int(data[0][0]) == 1:
            logging.error("Employee Already Assigned")
            return JSONResponse(content={"message":"Employee is already assigned a project"},status_code=200)
        
        #To check wether the manager exists or not for the project, Fetcing list of all the previous employees and adding the new employee in the list
        cursor_object.execute(f"SELECT employees_id FROM project_assigned WHERE project_id = '{project['project_id']}' AND managers_id IS NOT NULL")
        data = cursor_object.fetchall()
        check = len(data)
        if int(check) <= 0:
            logging.error("Unable to assign employee, manager doesn't exists")
            return JSONResponse(content={'message': 'Unable To Assigned Employee, Manager Doesnt Exists'},status_code=200)
        prev_employees_result = data[0]
        if prev_employees_result is not None:
            prev_employees = prev_employees_result[0]
            if prev_employees:
                prev_employees = json.loads(prev_employees)
            else:
                prev_employees = []
        else:
            prev_employees = []
        prev_employees.append(project['employee_id'])
        new_employees_json = json.dumps(prev_employees)

        #Updating the new employees list to the project_assigned table for the project_id
        cursor_object.execute(f"UPDATE project_assigned SET employees_id = %s WHERE project_id = %s", (new_employees_json, project['project_id']))

        #Updating the employee status for the employees_information table
        cursor_object.execute(f"UPDATE employees_information SET project_assigned = '{project['project_id']}',assigned = 1 WHERE id = '{project['employee_id']}'")
        connection.commit()
        logging.info(f"Project Assigned Successfulyy : {project['employee_id']}")
        return JSONResponse(content={'message': 'Project Assigned Successfully'},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally :
        disconnect(connection)