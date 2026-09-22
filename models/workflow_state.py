from pydantic import BaseModel

class State(BaseModel):
    Data_Extraction : list | None = None
    User_Service : str = ""
    User_Proof : str = ""
    User_Low_Risk : str = ""
    channel : str = ""
    current_step : str = ""
    status : str = ""
    research_result : dict | None = None
    strategy_result : dict | None = None
    outreach_result : dict | None = None
    Final_report : dict | None = None

state = State()
