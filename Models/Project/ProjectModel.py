from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
def validate_project_data(name, skills_required):
    if len(name) > 30 or len(name)==0 or len(skills_required)==0: 
        return "Input data exceeds allowed length"
class Project(Base):
    __tablename__ = 'project_information'
    project_id = Column(String(10), primary_key=True)
    project_name = Column(String(40))
    skills_required = Column(String(255))