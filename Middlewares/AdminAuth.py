import jwt
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ConnectSql import connect, disconnect

def is_token_expired(token):
    try:
        payload = jwt.decode(token, verify=False)  # Decode the token without verification
        expiration_time = payload['exp']
        current_time = datetime.utcnow().timestamp()
        return current_time > expiration_time
    except jwt.ExpiredSignatureError:
        return True  # Token has expired
    except jwt.InvalidTokenError:
        return True  # Invalid token

def admin_auth(user):
    #Check required parameters of request
    required_parameters = ['admin_id','token']
    if not all(param in user for param in required_parameters):
        return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)
    try:
        connection = connect()
        cursor_object = connection.cursor()
        cursor_object.execute(f"SELECT token,user_role FROM user_management WHERE id='{user['admin_id']}'")
        db_token = cursor_object.fetchone()
        if db_token is None:
            return JSONResponse(content={"message": "User not found"}, status_code=404)  
        token_expired = is_token_expired(user['token'])
        if token_expired:
            return JSONResponse(content={"message": "Unauthorized Access, Token expried"}, status_code=401) 
        if db_token[0] != user['token'] or db_token[1]!='admin':
            return JSONResponse(content={"message": "Unauthorized Access"}, status_code=403)  
        return JSONResponse(content={"message": "Authorized Access"}, status_code=200) 
    except Exception as e:
        print("Some Exception Occured",e)
        return JSONResponse(content={"message": "Internal Server Error"}, status_code=500) 
    finally:
        disconnect(connection)
            

