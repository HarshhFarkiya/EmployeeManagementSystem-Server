from ConnectSql import connect, disconnect
from Views.Employee import Employee
from fastapi import FastAPI
from fastapi.responses import JSONResponse
def filter_employees(skills):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Converting skills into lower case
        required_skills = skills.lower()
        keywords = required_skills.split()
        #Query to find all the details of a employee
        cursor_object.execute(f"SELECT * FROM employees_information")
        result = cursor_object.fetchall()
        employees=[]
        for e in result:
            curr_skills = e[4].lower()
            found=False
            for keyword in keywords:
                if keyword in curr_skills:
                    found=True
            if found:
                employees.append(e)
        all_employees = Employee.get_employee_response(employees)
        connection.commit()
        return JSONResponse(content={'message': 'Filtered Employees', 'result': all_employees},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)
