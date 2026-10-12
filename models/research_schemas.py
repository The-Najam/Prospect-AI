from pydantic import BaseModel, Field
from typing import Literal

class Evidence(BaseModel):
    quote: str
class Sourced(BaseModel):
    value: str
    evidence: Evidence

class Location(BaseModel):
    kind: Literal["headquarters", "office", "service_area"]
    value: str
    evidence: Evidence

class Person(BaseModel):
    name: str
    role: str
    evidence: Evidence

class ContactPath(BaseModel):
    channel: Literal["email", "form", "phone", "booking_link", "social", "other"]
    value: str
    evidence: Evidence

class Service(BaseModel):
    name: str
    evidence: Evidence

class CompanyData(BaseModel):
    name: Sourced | None = None
    about: Evidence | None = None
    industry: Sourced | None = None
    locations: list[Location] = []
    contact_paths: list[ContactPath] = []

class ResearchResult(BaseModel):
    company: CompanyData
    services: list[Service] = []
    business_type: Literal["b2b", "b2c", "both", "unclear"] = "unclear"
    business_type_evidence: Evidence | None = None
    people: list[Person] = []
    user_service: str | None = None
    user_proof: str | None = None
    user_low_risk: str | None = None

