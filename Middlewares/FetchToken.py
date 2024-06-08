import jwt
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ConnectSql import connect, disconnect

def fetch_token(id):
    connection = connect()
    try:
        cursor_object = connection.cursor()
        cursor_object.execute(f"SELECT token,user_role FROM user_management WHERE id='{id}'")
        db_token = cursor_object.fetchone()
        if db_token is None:
            return 404
        return db_token
    except Exception as e:
        print("Some Exception Occured",e)
        return JSONResponse(content={"message": "Internal Server Error"}, status_code=500) 
    finally:
        disconnect(connection)