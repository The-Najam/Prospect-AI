from pydantic import BaseModel
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


class ICP(BaseModel):
    Type : str
    location : str
    Needs : list[str]
    Buying_behavior : str
    Objections : str

class Opportunties(BaseModel):
    Pain_points : list[str]
    

class Research_result(BaseModel):
    CompanyData : Company_Data
    services : Services
    icp : ICP
    opportunties : Opportunties
    user_service: str = ""
    user_proof: str = ""
    user_low_risk: str = ""

