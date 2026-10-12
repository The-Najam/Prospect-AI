from enum import Enum
from pydantic import BaseModel
from typing import Literal, List


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
    qualification: Literal["strong", "medium", "low"]   # overall: is this prospect worth contacting?
    fit: Literal["strong", "moderate", "weak", "insufficient_evidence"]  # how well they match the user's service
    fit_reasons: List[str]
    offer: Offer
    angle: Outreach_Angle
    reasoning: Reasoning
    channel: str = ""    # provided by user
    service: str         # provided by user
    proof: str           # provided by user


