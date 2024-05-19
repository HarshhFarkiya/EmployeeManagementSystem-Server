from Models.Project.ProjectModel import Project;
from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
def delete_project(id):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Check Project Exists or Not
        cursor_object.execute(f"SELECT * FROM project_information WHERE project_id='{id}'")
        prj = cursor_object.fetchall()
        check=len(prj)
        if check<=0:
            return JSONResponse(content={"message": "Project Doesnt Exists"}, status_code=404)

        
        cursor_object.execute(f"SELECT managers_id,employees_id from project_assigned WHERE project_id='{id}'")
        result = cursor_object.fetchone()
        all_employees = result[1]
        all_managers=result[0]
        all_employees_list=json.loads(all_employees)


        # Create a string for the IN clause
        remove_emps = ','.join(["'{}'".format(emp) for emp in all_employees_list])
        cursor_object.execute(f"UPDATE employees_information SET assigned=0,project_assigned=NULL WHERE id IN({remove_emps})")


        #Fetch all the managers and employees of the project and then remove the project id from the assinged column
        #Lets first remove from the employee table
        values_list = eval(all_managers)
        for ele in values_list:
            cursor_object.execute(f"SELECT projects_assigned FROM managers_information WHERE id='{ele}'")
            projects_assigned_manager = cursor_object.fetchone()[0]
            projects_assigned_manager_list= json.loads(projects_assigned_manager)
            if id in projects_assigned_manager_list:
                projects_assigned_manager_list.remove(id)
            projects_assigned_manager_list_json = json.dumps(projects_assigned_manager_list)
            cursor_object.execute(f"UPDATE managers_information SET projects_assigned=%s WHERE id=%s",(projects_assigned_manager_list_json,ele))
        cursor_object.execute(f"DELETE FROM project_assigned WHERE project_id='{id}'")
        cursor_object.execute(f"DELETE FROM project_information WHERE project_id='{id}'")
        connection.commit()
        return JSONResponse(content={"message": "manager Deleted Successfully"}, status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally :
        disconnect(connection)
