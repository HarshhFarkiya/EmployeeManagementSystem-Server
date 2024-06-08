from Models.Project.ProjectModel import Project,validate_project_data;
from ConnectSql import connect, disconnect
from fastapi import FastAPI
from fastapi.responses import JSONResponse
def add_project(project):
    #Connection Creation With SQL
    connection = connect()
    cursor_object = connection.cursor()
    try:
        #Check all the required parameters exists in request or not
        required_parameters = ['project_name','skills_required']
        if not all(param in project for param in required_parameters):
            return JSONResponse(content={"message": "Missing Parameters"}, status_code=422)

        if validate_project_data(project['project_name'],project['skills_required'])=="Input data exceeds allowed length":
            return JSONResponse(content={'message': 'Input data exceeds allowed length'},status_code=422)
        #Query to find the new project id
        cursor_object.execute("SELECT projects FROM users_count")
        result = cursor_object.fetchone()
        id=int(result[0]) + 1

        
        #To check wether the employee already exists or not
        cursor_object.execute(f"SELECT * FROM project_information WHERE project_name = '{project['project_name']}'")
        check = len(cursor_object.fetchall())
        if int(check) > 0:
            return JSONResponse(content={'message':'Project Already Exists'},status_code=409)
        new_project = Project(project_id=id,project_name = project['project_name'], skills_required=project['skills_required'])
        cursor_object.execute(f"INSERT INTO project_information VALUES ('PRJ{new_project.project_id}', '{new_project.project_name}', '{new_project.skills_required}')")
        cursor_object.execute(f"INSERT INTO project_assigned VALUES ('PRJ{new_project.project_id}' , NULL, NULL)")
        cursor_object.execute(f"UPDATE users_count SET projects={id}")
        connection.commit()
        return JSONResponse(content={'message': 'Project Added Successfully', 'project_id': 'PRJ'+str(new_project.project_id)},status_code=200)
    except Exception as e: 
        print("Some Error Occured", e)
        disconnect(connection)
        raise Exception("Internal Server Error",e)
    finally :
        disconnect(connection)
