from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
def add_skills(employee):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Checking all the required parameters are present or not in the request
        required_parameters = ['employee_id','add_skills']
        if not all(param in employee for param in required_parameters):
            return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)

        new_skills = employee['add_skills']
        #Updating the new skills to the employees_information table
        cursor_object.execute(f"UPDATE employees_information SET skills='{new_skills}' WHERE id='{employee['employee_id']}'")
        connection.commit()
        return JSONResponse(content={"message": "Skills Added"}, status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)
