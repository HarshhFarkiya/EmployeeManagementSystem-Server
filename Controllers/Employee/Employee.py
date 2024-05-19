from Models.Employee.EmployeeModel import Employee;
from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import bcrypt

def add_employee(employee):
    #Status : Assigned/Unassigned
    emp_status=False
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Check all the required parameters are prsenet or not in the request
        required_parameters = ['name','email','skills','phone','experience_years']
        if not all(param in employee for param in required_parameters):
            return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)


        #Query to find the new employee id
        cursor_object.execute("SELECT employees FROM users_count")
        result = cursor_object.fetchall()
        emp_id=int(result[0][0]) + 1


        #To check wether the employee already exists or not
        cursor_object.execute(f"SELECT * FROM employees_information WHERE email = '{employee['email']}'")
        check = len(cursor_object.fetchall())
        if int(check) > 0:
            return JSONResponse(content={"message": "Employee already exists"}, status_code=409)

        #Creating new employee object from the Employee Model
        new_employee = Employee(id=emp_id,name = employee['name'], email=employee['email'], phone = employee['phone'],skills=employee['skills'],assigned=emp_status,experience_years=employee['experience_years'],project_assigned="")

        #Adding the new employee in the employees_information table
        cursor_object.execute(f"INSERT INTO employees_information VALUES ('EMP{new_employee.id}', '{new_employee.name}', '{new_employee.email}', '{new_employee.phone}', '{new_employee.skills}', {new_employee.assigned}, {new_employee.experience_years} , '{new_employee.project_assigned}')")

        #Creating a system generated password for the employee
        password = new_employee.email +"@"+ str(new_employee.id)

        #Creating the hashed password for the system generated password 
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        #Creating the escaped password to store in database
        escaped_password = connection.converter.escape(hashed_password.decode())

        #Inserting the user credentials in the user_management table
        cursor_object.execute(f"INSERT INTO user_management VALUES ('EMP{new_employee.id}' , '{new_employee.email}' , '{escaped_password}', 'employee' , NULL)")

        #Updating new id for the next employee
        cursor_object.execute(f"UPDATE users_count SET employees={emp_id}")
        connection.commit()
        return JSONResponse(content={'message': 'User Added Successfully', 'employee_id': 'EMP'+str(new_employee.id), 'password': password},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)
