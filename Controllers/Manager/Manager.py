from Models.Manager.ManagerModel import Manager,validate_manager_data;
from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import bcrypt
import logging
def add_manager(manager):
    emp_status=False
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Check the required parameters are exists or not in the request
        required_parameters = ['email','phone','name']
        if not all(param in manager for param in required_parameters):
            logging.error("Missing Parameters")
            return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)

        #Validating new manager
        if validate_manager_data(manager['name'],manager['email'],manager['phone'])=="Input data exceeds allowed length":
            logging.error("Input Exceeds Allowed Length")
            return JSONResponse(content={'message': 'Input data exceeds allowed length'},status_code=422)

        #Fetching the id for new manager to be add
        cursor_object.execute("SELECT managers FROM users_count")
        result = cursor_object.fetchone()
        id=int(result[0]) + 1

        #Check wether the email or user is already exists or not
        cursor_object.execute(f"SELECT * FROM managers_information WHERE email = '{manager['email']}'")
        check = len(cursor_object.fetchall())
        if int(check) > 0:
            logging.info("User Exists")
            return JSONResponse(content={'message' : 'User Already Exists'},status_code=409)

        #If not then pass the manager into the Manager Model in order to get object of new manager
        new_manager = Manager(id=id,name = manager['name'], email=manager['email'], phone = manager['phone'])

        #Insert the new manager into the managers_information table
        cursor_object.execute(f"INSERT INTO managers_information VALUES ('MNG{new_manager.id}', '{new_manager.name}', '{new_manager.email}', '{new_manager.phone}',NULL)")

        #Creating a password
        password = new_manager.email +"@"+ str(new_manager.id)

        #Hashing the password and then convert into escaped format to store in db
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        escaped_password = connection.converter.escape(hashed_password.decode())

        #Store the credentials in the user_management table
        cursor_object.execute(f"INSERT INTO user_management VALUES ('MNG{new_manager.id}' , '{new_manager.email}' , '{escaped_password}', 'manager', NULL)")
        cursor_object.execute(f"UPDATE users_count SET managers={id}")
        connection.commit()
        logging.info("User Added")
        return JSONResponse(content={'message': 'User Added Successfully', 'manager_id': new_manager.id, 'password': password},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        logging.error(e)
        return JSONResponse(content={'message': 'Some Error Occured'},status_code=500)
        raise Exception("Internal Server Error",e)
    finally:
        disconnect(connection)
