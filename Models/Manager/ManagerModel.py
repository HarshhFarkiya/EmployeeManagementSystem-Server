from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
def validate_manager_data(name, email, phone):
    if len(name) > 30 or len(name) ==0 or len(email)==0 or len(email) > 40 or len(phone) !=10: 
        return "Input data exceeds allowed length"

class Manager(Base):
    __tablename__ = 'managers_information'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), index=True)
    email = Column(String)
    phone = Column(String)