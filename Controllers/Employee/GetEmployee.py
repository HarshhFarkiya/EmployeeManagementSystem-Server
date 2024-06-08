from ConnectSql import connect, disconnect
from Views.Employee import Employee
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging 

def get_employee(id):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Query to find all the details of a employee
        cursor_object.execute(f"SELECT * FROM employees_information WHERE id='{id}'")
        result = cursor_object.fetchall()
        all_employees = Employee.get_employee_response(result)
        connection.commit()
        logging.info("Employee Fetched Successfully")
        return JSONResponse(content={'message': 'Employee Details Fetched Successfully', 'result': all_employees},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        logging.error(e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    disconnect(connection)
