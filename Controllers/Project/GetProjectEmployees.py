from ConnectSql import connect, disconnect
from Views.Employee import Employee
from Views.Manager import Manager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
def get_project_employees(project_id):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Check project exists or not
        cursor_object.execute(f"SELECT * FROM project_information WHERE project_id='{project_id}'")
        check = len(cursor_object.fetchone())
        if check is None:
            return JSONResponse(content=f"{'message': 'Invalid Project Id'}",status_code=404)

        
        #Query to find all the details of a employee
        cursor_object.execute(f"SELECT managers_id,employees_id FROM project_assigned WHERE project_id='{project_id}'")
        result = cursor_object.fetchone()

        #Getting all the manager's id and then converitng them to list
        managers_id=result[0]
        managers_id_list=[]
        all_managers=[]
        if managers_id is not None:
            cleaned_string = managers_id.strip('[]').strip()
            managers_id_list = [element.strip('" ') for element in cleaned_string.split(',')]
            #Converting the list into format that SQl Query accepts
            placeholders = ",".join(["%s"] * len(managers_id_list))
            cursor_object.execute(f"SELECT * FROM managers_information WHERE id IN ({placeholders})", managers_id_list)
            #Calling manager view to fomat the output view
            all_managers = Manager.get_manager_response(cursor_object.fetchall())


        #Getting all the employee's id and then converitng them to list
        employees_id=result[1]
        employees_id_list=[]
        all_employees=[]
        if employees_id is not None:
            cleaned_string = employees_id.strip('[]').strip()
            employees_id_list = [element.strip('" ') for element in cleaned_string.split(',')]
            #Converting the list into format that SQl Query accepts
            placeholders = ",".join(["%s"] * len(employees_id_list))
            cursor_object.execute(f"SELECT * FROM employees_information WHERE id IN ({placeholders})", employees_id_list)
            #Calling manager view to fomat the output view
            all_employees = Employee.get_employee_response(cursor_object.fetchall())
        connection.commit()
        return JSONResponse(content={'message': 'Employee Details Fetched Successfully', 'result': {'managers' : all_managers, 'employees': all_employees}},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)
