from pydantic import BaseModel, Field
from enum import Enum
from typing import List



class Service(BaseModel):
    name : str
    description : str
    Pricing : str
    

class Company_Data(BaseModel):
    name : str
    about : str
    location : str 
    industry : str
    Company_size : str 


class Services(BaseModel):
    services : List[Service]


class CustomerType(str, Enum):
    B2B = "B2B"
    B2C = "B2C"
    Both = "Both"
    Unknown = "Unknown"
 

class ICP(BaseModel):
    Type : CustomerType
    location : str
    General_Buying_behavior : str
    General_Objections : str

class Opportunties(BaseModel):
    Pain_points : list[dict]
    

class Research_result(BaseModel):
    CompanyData : Company_Data
    services : Services
    icp : ICP
    opportunties : Opportunties
    user_service: str = ""
    user_proof: str = ""
    user_low_risk: str = ""

