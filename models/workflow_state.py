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
    total_token_used : int = 0
    input_tokens : int = 0
    output_tokens : int = 0

state = State()
