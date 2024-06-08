from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Models.Employee.EmployeeModel import Employee,validate_employee_data;
import logging



def update_employee_information(employee):
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Checking all the reuired parameters exists or not in request
        required_parameters = ['employee_id', 'name','email','phone', 'skills','experience_years']
        if not all(param in employee for param in required_parameters):
            logging.error("Missing Parameters")
            return JSONResponse(content={'message': 'Missing required parameters'},status_code=422)
        new_employee_inforamtion={'employee_id':employee['employee_id'],'name':employee['name'],'email':employee['email'],'phone':employee['phone'],'skills':employee['skills']}
        #Check wehter the employee exists or not
        cursor_object.execute(f"SELECT * FROM employees_information WHERE id='{employee['employee_id']}'")
        check = cursor_object.fetchall()
        if len(check)<=0 :
            logging.error("Invalid Employee Id")
            return JSONResponse(content={'message' : 'Employee Id doesnt exists'},status_code=404)
        
        new_employee = Employee(id=employee['employee_id'],name = employee['name'], email=employee['email'], phone = employee['phone'],skills=employee['skills'],experience_years=employee['experience_years'])
        if validate_employee_data(employee['name'],employee['email'],employee['phone'],employee['skills'],"") == "Input data exceeds allowed length":
            logging.error("Input Exceeds Allowed Length")
            return JSONResponse(content={'message': 'Input data exceeds allowed length'},status_code=422)

        #If employee exists then update the employee details
        cursor_object.execute(f"UPDATE employees_information SET name=%s,email=%s,phone=%s,skills=%s WHERE id=%s",(new_employee.name,new_employee.email,new_employee.phone,new_employee.skills,new_employee.id))
        connection.commit()
        logging.info("Profile Updated Successfully")
        return JSONResponse(content={'message': 'Profile Updated successfully'},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        logging.error(e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)
