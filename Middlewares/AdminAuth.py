import jwt
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ConnectSql import connect, disconnect
from Middlewares.CheckTokenExpiration import is_token_expired;
from Middlewares.FetchToken import fetch_token;


def admin_auth(user):
    #Check required parameters of request
    required_parameters = ['admin_id','token']
    if not all(param in user for param in required_parameters):
        return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)
    try:
        response = fetch_token(user['admin_id'])
        if response == 404:
            return JSONResponse(content={"message": "User not found"}, status_code=404)  
        token_expired = is_token_expired(user['token'])
        if token_expired:
            return JSONResponse(content={"message": "Unauthorized Access, Token expried"}, status_code=401) 
        if response[0] != user['token'] or response[1]!='admin':
            return JSONResponse(content={"message": "Unauthorized Access"}, status_code=403)  
        return JSONResponse(content={"message": "Authorized Access"}, status_code=200) 
    except Exception as e:
        print("Some Exception Occured",e)
        return JSONResponse(content={"message": "Internal Server Error"}, status_code=500) 