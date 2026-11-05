from pydantic import BaseModel, HttpUrl, field_validator
from research.data_extraction import validate_prospect_url


class GetInput(BaseModel):
    url : HttpUrl
    user_service : str 
    low_risk_offer : str
    proof : str | None
    channel : str

    @field_validator("url", mode="before")
    @classmethod
    def validate_prospect_website(cls, value: object) -> object:
        if not isinstance(value, str):
            raise ValueError("Enter a complete HTTP or HTTPS website URL.")
        validate_prospect_url(value)
        return value