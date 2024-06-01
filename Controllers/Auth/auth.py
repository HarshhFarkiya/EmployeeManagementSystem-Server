from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import bcrypt
from typing import Dict
import jwt
from datetime import datetime, timedelta
import logging
#Seacret key for jwt token
SECRET_KEY = "employee_management_system"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Function to create a access token
def create_access_token(data: Dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt.decode("utf-8")  


#Function to authenticate user during login
def auth_user(UserId, password):
    try:
        #Creating Connection With SQL
        connection = connect()
        cursor_object = connection.cursor()

        # Check if the user exists
        query = f"SELECT user_role,emp_password,id FROM user_management WHERE email='{UserId}'"
        cursor_object.execute(query)
        data = cursor_object.fetchall()
        if len(data) <= 0:
            logging.error("User Doesn't exists")
            return JSONResponse(content={"message":"User Doesn't Exist"}, status_code=404)
        # Check if the password is correct
        result = data[0]
        hashed_password = result[1]
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            #If password is correct then we create a access token and assign it to the user
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token({"sub": UserId},access_token_expires)
            cursor_object.execute(f"UPDATE user_management SET token='{access_token}' WHERE id='{result[2]}'")
            data = {"user_id":result[2],"role":result[0],"token":access_token}
            connection.commit()
            logging.info("User Logged In")
            return JSONResponse(content=data, status_code=200)
        logging.error("Invalid Password")
        return JSONResponse(content={"message":"Invalid Password"}, status_code=401)

    except Exception as e:
        print(e)
        logging.error(f"Login Error : {e}")
        return JSONResponse(content="Internal Server Error", status_code=500)
    finally:
        disconnect(connection)

