from enum import Enum
from pydantic import BaseModel
from typing import List



class Qualification(str, Enum):
    strong = "strong"
    medium = "medium"
    weak = "weak"

class Fit(str, Enum):
    strong = "strong"
    moderate = "moderate"
    weak = "weak"
    unclear = "unclear"


class Opportunity(BaseModel):
    pain : List[str]
    fit : Fit
    score : int


class Offer(BaseModel):
    problem : str
    desirable_outcome : str
    proof : str
    low_risk : str
    value : str


class Reasoning(BaseModel):
    reason : List[str]


class Outreach_Angle(BaseModel):
    hooks : List[str]
    angle : str
    cta : str


class Strategy_result(BaseModel):
    qualification : Qualification
    opportunity : Opportunity
    offer : Offer
    reason : Reasoning
    angle : Outreach_Angle
    channel : str = ""


