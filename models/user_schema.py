from pydantic import BaseModel, HttpUrl


class GetInput(BaseModel):
    url : HttpUrl
    user_service : str 
    low_risk_offer : str
    proof : str | None
    channel : str