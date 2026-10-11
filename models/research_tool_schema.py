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

    
class PainPoint(BaseModel):
    Pain_Point: str
    Evidence: str          # link; code checks it is one of the search result URLs

class WebSearchResult(BaseModel):
    pain_points: List[PainPoint] = []
    available_solutions: List[str] = []
    satisfied: bool | None = None     # None = not enough evidence to say
    resources: List[str] = []  


class ExtraPage(BaseModel):
    url: str
    page_type: str
    content: str


class additional_research(BaseModel):
    additional_info : list[ExtraPage] = Field(
        description="List of additional research findings, each with a URL, page type, and content.")


class AdditionalResearchInput(BaseModel):
    url: str
    missing_fields: list[str]
    already_fetched: list[str]


class offer_tool_input(BaseModel):
    pain : List[str]
    problem : str
    desirable_outcome : str
    proof : str
    low_risk : str
    value : str

class offer_refine(BaseModel):
    refine_offer : str