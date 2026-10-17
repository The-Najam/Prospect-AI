from typing import TypedDict, Annotated
import operator

class WorkflowState(TypedDict):
    prospect_url : str
    user_service : str
    low_risk_offer : str
    proof : str | None
    channel : str
    page_content : list[dict]
    links : list
    cleaned_content : dict | list[dict]
    content_status : str
    research_status : str
    research_result : dict | None
    strategy_result : dict | None
    strategy_status : str
    outreach_result : dict | None
    outreach_status : str
    final_report : dict | None
    cleaned_content_attempts : int
    research_attempts : int 
    strategy_attempts : int
    outreach_attempts : int
    max_attempts : int







