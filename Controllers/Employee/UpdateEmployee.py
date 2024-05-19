from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse

def update_employee_information(employee):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Checking all the reuired parameters exists or not in request
        required_parameters = ['employee_id', 'name','email','phone', 'skills','experience_years']
        if not all(param in employee for param in required_parameters):
                return JSONResponse(content={'message': 'Missing required parameters'},status_code=422)
        new_employee_inforamtion={'employee_id':employee['employee_id'],'name':employee['name'],'email':employee['email'],'phone':employee['phone'],'skills':employee['skills']}
        #Check wehter the employee exists or not
        cursor_object.execute(f"SELECT * FROM employees_information WHERE id='{employee['employee_id']}'")
        check = cursor_object.fetchall()
        if len(check)<=0 :
            return f"{{'message' : 'Employee Id doesn't exists'}}"
        #If employee exists then update the employee details
        cursor_object.execute(f"UPDATE employees_information SET name=%s,email=%s,phone=%s,skills=%s WHERE id=%s",(new_employee_inforamtion['name'],new_employee_inforamtion['email'],new_employee_inforamtion['phone'],new_employee_inforamtion['skills'],new_employee_inforamtion['employee_id']))
        connection.commit()
        return JSONResponse(content={'message': 'Profile Updated successfully'},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)
