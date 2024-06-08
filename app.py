from fastapi import FastAPI ,Request
from Controllers.Employee import GetEmployees,GetEmployee, AddSkills,UpdateEmployee,UnassignProject as UnassignProjectEmployee,AssignProject as AssignProjectEmployee,Employee as emp,Filter,DeleteEmployee
from Controllers.Manager import AssignProject as AssignProjectManager,UnassignProject as UnassignProjectManager,GetManagers,GetManager,Manager,RequestResources,DeleteManager
from Controllers.Project import Project,GetProjects,GetProject,GetProjectEmployees,DeleteProject
from Controllers.Auth import auth
from Controllers.Admin import GetResourcesRequest,ApproveRequest,RejectRequest,AddAdmin
from fastapi.middleware.cors import CORSMiddleware
from Middlewares import EmployeeAuth,ManagerAuth,AdminAuth,UserAuth
import logging
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
logging.basicConfig(
       filename='app.log',  # Log file name
       level=(logging.DEBUG),  # Log level (e.g., DEBUG, INFO, ERROR)
       format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)
@app.post("/addEmployee")
def add_employee(employee : dict):
    middleware_verification = AdminAuth.admin_auth(employee)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = emp.add_employee(employee)
    return result

@app.post("/addManager")
def add_manager(manager : dict):
    middleware_verification = AdminAuth.admin_auth(manager)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = Manager.add_manager(manager)
    return result

@app.post("/addProject")
def add_project(project : dict):
    middleware_verification = AdminAuth.admin_auth(project)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = Project.add_project(project)
    return result

@app.get("/getProjects")
def get_all_projects(request:Request):
    query_params = dict(request.query_params)
    token = query_params.get("token")
    uid = query_params.get("id")
    user={"token":token,"id":uid}
    middleware_verification = UserAuth.user_auth(user)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = GetProjects.get_all_projects()
    return result

@app.get("/getProject")
def get_all_projects(request:Request):
    query_params = dict(request.query_params)
    token = query_params.get("token")
    uid = query_params.get("id")
    user={"token":token,"id":uid}
    middleware_verification = UserAuth.user_auth(user)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    query_params = dict(request.query_params)
    result = GetProject.get_project(query_params.get('project_id'))
    return result

@app.post("/authentication")
def auth_user(user : dict):
    result = auth.auth_user(user['UserId'] , user['password'])
    return result

@app.post("/assignEmployee")
def assign_project_employee(details : dict):
    middleware_verification = AdminAuth.admin_auth(details)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = AssignProjectEmployee.assign_project_employee(details)
    return result

@app.delete("/unassignEmployee")
def unassign_project_employee(details : dict):
    middleware_verification = AdminAuth.admin_auth(details)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = UnassignProjectEmployee.unassign_project_employee(details)
    return result

@app.post("/assignManager")
def assign_project_employee(details : dict):
    middleware_verification = AdminAuth.admin_auth(details)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = AssignProjectManager.assign_project_manager(details)
    return result

@app.delete("/unassignManager")
def assign_project_employee(details : dict):
    middleware_verification = AdminAuth.admin_auth(details)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = UnassignProjectManager.unassign_project_manager(details)
    return result

@app.get("/getEmployees")
def get_employees(request:Request):
    query_params = dict(request.query_params)
    token = query_params.get("token")
    uid = query_params.get("id")
    user={"token":token,"id":uid}
    middleware_verification = UserAuth.user_auth(user)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = GetEmployees.get_all_employees()
    return result

@app.get("/getEmployee")
def get_employees(request: Request):
    query_params = dict(request.query_params)
    token = query_params.get("token")
    uid = query_params.get("id")
    user={"token":token,"id":uid}
    middleware_verification = UserAuth.user_auth(user)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    query_params = dict(request.query_params)
    result = GetEmployee.get_employee(query_params.get('employee_id'))
    return result

@app.get("/getManagers")
def get_managers(request:Request):
    query_params = dict(request.query_params)
    token = query_params.get("token")
    uid = query_params.get("id")
    user={"token":token,"id":uid}
    middleware_verification = UserAuth.user_auth(user)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = GetManagers.get_all_managers()
    return result

@app.get("/getManager")
def get_manager(request:Request):
    query_params = dict(request.query_params)
    token = query_params.get("token")
    uid = query_params.get("id")
    user={"token":token,"id":uid}
    middleware_verification = UserAuth.user_auth(user)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    query_params = dict(request.query_params)
    result = GetManager.get_manager(query_params.get('manager_id'))
    return result

@app.get("/getProjectEmployees")
def get_project_employees(request:Request):
    status=False
    query_params = dict(request.query_params)
    token = query_params.get("token")
    uid = query_params.get("id")
    user={"token":token,"id":uid}
    middleware_verification = UserAuth.user_auth(user)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result = GetProjectEmployees.get_project_employees(query_params.get('project_id'))
    return result

@app.put("/addSkills")
def add_skills(employee:dict):
    middleware_verification = EmployeeAuth.employee_auth(employee)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result=AddSkills.add_skills(employee)
    return result

@app.put("/updateEmployee")
def update_employee(employee:dict):
    middleware_verification = AdminAuth.admin_auth(employee)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result=UpdateEmployee.update_employee_information(employee)
    return result

@app.post("/requestResource")
def request_resource(request:dict):
    middleware_verification = ManagerAuth.manager_auth(request)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result=RequestResources.request_resource(request)
    return result

@app.get("/getResourceRequests")
def get_all_requests(request:Request):
    query_params = dict(request.query_params)
    token = query_params.get("token")
    uid = query_params.get("id")
    user={"token":token,"admin_id":uid}
    print(uid,token)
    middleware_verification = AdminAuth.admin_auth(user)
    if middleware_verification.status_code != 200 :
        return middleware_verification   
    result=GetResourcesRequest.get_all_requests()
    return result

@app.put("/approveRequest")
def approve_request(request:dict):
    middleware_verification = AdminAuth.admin_auth(request)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result=ApproveRequest.approve_request(request)
    return result

@app.put("/rejectRequest")
def reject_request(request:dict):
    middleware_verification = AdminAuth.admin_auth(request)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    result=RejectRequest.reject_request(request)
    return result

@app.get("/filter")
def filter_employees(request:Request,user:dict):
    middleware_verification = UserAuth.user_auth(user)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    query_params = dict(request.query_params)
    result=Filter.filter_employees(query_params.get("skills"))
    return result

@app.delete("/removeEmployee")
def remove_employee(request:Request,admin:dict):
    middleware_verification = AdminAuth.admin_auth(admin)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    query_params = dict(request.query_params)
    result=DeleteEmployee.delete_employee(query_params.get("employee_id"))
    return result

@app.delete("/removeManager")
def remove_employee(request:Request,admin:dict):
    middleware_verification = AdminAuth.admin_auth(admin)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    query_params = dict(request.query_params)
    result=DeleteManager.delete_manager(query_params.get("manager_id"))
    return result


@app.delete("/removeProject")
def remove_employee(request:Request,admin:dict):
    middleware_verification = AdminAuth.admin_auth(admin)
    if middleware_verification.status_code != 200 :
        return middleware_verification
    query_params = dict(request.query_params)
    result=DeleteProject.delete_project(query_params.get("project_id"))
    return result