from Models.Project.ProjectModel import Project;
from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json 
import logging 

def delete_employee(id):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Check wether employee id exists or not
        cursor_object.execute(f"SELECT * FROM employees_information WHERE id='{id}'")
        emp = cursor_object.fetchall()
        check=len(emp)
        if check<=0:
            logging.error("Employee doesn't exists")
            return JSONResponse(content={"message": "Employee Doesnt Exists"}, status_code=404)
        
        #If exists then check wether employee is assigned to any project or not
        status=emp[0][5]
        if int(status) == 1:
            logging.error("Unassign employee from project before deletion")
            return JSONResponse(content={"message": "Employee already assigned to a project, Unassign before delete the user"}, status_code=200)

        #If not assigned then we delete employee from employees_information and user_management tables
        cursor_object.execute(f"DELETE FROM employees_information WHERE id='{id}'")
        cursor_object.execute(f"DELETE FROM user_management WHERE id='{id}'")
        connection.commit()
        logging.info("Employee Deleted Successfully")
        return JSONResponse(content={"message": "Employee Deleted Successfully"}, status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        logging.error(e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally :
        disconnect(connection)
