from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees_information'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10))
    email = Column(String(10))
    phone = Column(String(10))
    skills = Column(String(10))
    assigned = Column(Boolean)
    experience_years = Column(Integer)
    project_assigned = Column(String(10))
