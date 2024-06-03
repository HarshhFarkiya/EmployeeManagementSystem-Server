from Models.Project.ProjectModel import Project;
from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

def delete_manager(id):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Check wether that manager exists or not
        cursor_object.execute(f"SELECT * FROM managers_information WHERE id='{id}'")
        emp = cursor_object.fetchall()
        check=len(emp)
        if check<=0:
            logging.error("Missing Parameters")
            return JSONResponse(content={"message": "Manager Doesnt Exists"}, status_code=404)

        #Check wehter employee is assigned to any project or not
        status=emp[0][4]
        if status is not None :
            logging.error("Manager already assgined")
            return JSONResponse(content={"message": "manager already assigned to a project, Unassign before delete the user"}, status_code=200)

        #If not then delete the manager
        cursor_object.execute(f"DELETE FROM managers_infoFetchingrmation WHERE id='{id}'")
        cursor_object.execute(f"DELETE FROM user_management WHERE id='{id}'")
        connection.commit()
        logging.info("Manager deleted")
        return JSONResponse(content={"message": "manager Deleted Successfully"}, status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        logging.error(e)
        raise Exception("Internal Server Error",e)
    finally :
        disconnect(connection)
