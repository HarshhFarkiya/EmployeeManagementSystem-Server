from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
def validate_employee_data(name, email, phone, skills, project_assigned):
    if len(name) > 30 or len(name)==0 or len(email) > 40 or len(email)==0 or len(phone)!=10 or len(skills) ==0 or len(skills) > 100 or len(project_assigned) > 10: 
        return "Input data exceeds allowed length"

class Employee(Base):
    __tablename__ = 'employees_information'
    id = Column(String(10), primary_key=True, index=True)
    name = Column(String(30))
    email = Column(String(40))
    phone = Column(String(10))
    skills = Column(String(100))
    assigned = Column(Boolean)
    experience_years = Column(Integer)
    project_assigned = Column(String(10))