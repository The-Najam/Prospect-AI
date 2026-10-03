from pydantic import BaseModel, Field
from typing import List

class social_media_extractor(BaseModel):
    social_urls : list[str] = Field(
        description="List of social media profile URLs to extract bio information from."
    )

class Bio_Extractor(BaseModel):
    url : str
    platform : str | None
    bio : str | None
    success : bool

class Platforms(BaseModel):
    bio_extractor : list[Bio_Extractor]

    
class  SearchWeb(BaseModel):
    pain_points : list[dict]
    avilable_solutions : list[str]
    satisfied : bool
    resources : list[str]


class additional_research(BaseModel):
    additional_info : list[str]


class offer_tool_input(BaseModel):
    pain : List[str]
    urgency : str
    problem : str
    desirable_outcome : str
    proof : str
    low_risk : str
    value : str

class offer_refine(BaseModel):
    refine_offer : str