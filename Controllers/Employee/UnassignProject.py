from ConnectSql import connect, disconnect
import json 
from fastapi import FastAPI
from fastapi.responses import JSONResponse
def unassign_project_employee(employee):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        required_parameters = ['employee_id']
        if not all(param in employee for param in required_parameters):
            return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)
        cursor_object.execute(f"SELECT * FROM employees_information WHERE id = '{employee['employee_id']}'")
        check = len(cursor_object.fetchall())
        if int(check) <= 0:
            return JSONResponse(content={"message":"Employee Doesn't Exists, Please Provide a Valid Employee Id"},status_code=404)
        
        #TO check wether employee is previoudly assigned any project
        cursor_object.execute(f"SELECT assigned,project_assigned FROM employees_information WHERE id = '{employee['employee_id']}'")
        emp_detail = list(cursor_object.fetchone())
        print(emp_detail)
        status = emp_detail[0]
        if status ==0:
            return JSONResponse(content={"message":"Employee is Already Unassigned"},status_code=409)
        
        #Get the assigned project's Id
        project_id = emp_detail[1]

        #Now unassign the employee in employee_information table
        cursor_object.execute(f"UPDATE employees_information SET assigned=0, project_assigned=NULL WHERE id = '{employee['employee_id']}'")

        #Now Check wether the project id exsits or not
        cursor_object.execute(f"SELECT * FROM project_information WHERE project_id = '{project_id}'")
        check = len(cursor_object.fetchall())
        if int(check) <= 0:
            return JSONResponse(content={"message":"Project Doesn't Exists, Please Provide a Valid Active Project Id"},status_code=404)

        #Now remove the employee id from the project_assigned table
        cursor_object.execute(f"SELECT employees_id FROM project_assigned WHERE project_id='{project_id}'")
        prev_employees_result = cursor_object.fetchone()
        if prev_employees_result is not None:
            prev_employees = prev_employees_result[0]
            if prev_employees:
                prev_employees = json.loads(prev_employees)
            else:
                prev_employees = []
        else:
            prev_employees = []
        if employee['employee_id'] in prev_employees:
            prev_employees.remove(employee['employee_id'])
        new_employees_json = json.dumps(prev_employees)
        if len(prev_employees)==0:
            new_employees_json=None

        #Updating the employees information to project_assigned table
        cursor_object.execute(f"UPDATE project_assigned SET employees_id = %s WHERE project_id = %s", (new_employees_json, project_id))
        connection.commit()
        return JSONResponse(content={'message': 'Project Unssigned Successfully'},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally :
        disconnect(connection)