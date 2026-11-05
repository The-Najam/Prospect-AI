# importing Libraries

from fastapi import FastAPI, BackgroundTasks, Request, HTTPException
from models.user_schema import GetInput
from models.workflow_state import WorkflowState
from orchestrator import inputdata, workflow
from research.data_extraction import validate_prospect_url
from database.database_operations import get_report as fetch_report
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware
from config.settings import setting
import selectors
import asyncio
import uuid
from uuid import UUID



# creating an app
app = FastAPI()

# enable and configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=setting.CORS_ORIGINS,  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# get the client's IP address from an incoming HTTP request
def get_client_ip(request: Request) -> str:
    if request.client and request.client.host in ("127.0.0.1", "::1"):
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

    return request.client.host if request.client else "unknown"


# creating the Rate Limit 
limiter = Limiter(key_func=get_client_ip)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
app.add_middleware(SlowAPIMiddleware)


# create report 
def generate_report(initial_state):
    state = WorkflowState(initial_state)
    result = asyncio.run(
    workflow(state),
    loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()),
)
    if result is not None:
        return {"report": result["state"].get("final_report")}


# get input request from the frontend
@app.post("/get_input")
@limiter.limit("10/hour")
def get_input(
    request: Request,
    data: GetInput,
    bg_task: BackgroundTasks,
):
    try:
        validate_prospect_url(str(data.url))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    initial_state = {
        "run_id": str(uuid.uuid4()),
        "prospect_url": str(data.url),
        "user_service":data.user_service,
        "low_risk_offer":data.low_risk_offer,
        "proof": data.proof,
        "channel":data.channel,
        "page_content": [],
        "links": [],
        "cleaned_content": [],
        "content_status": "",
        "research_result": {},
        "research_status": "",
        "strategy_result": {},
        "strategy_status": "",
        "outreach_result": {},
        "outreach_status": "",
        "final_report": {},
        "cleaned_content_attempts": 0,
        "research_attempts": 0,
        "strategy_attempts": 0,
        "outreach_attempts": 0,
        "max_attempts": 3,
        "gemini_tokens":0,
        "groq_tokens":0,
        "phase":"initial"
        ,"error_message": None
    }
    bg_task.add_task(
        generate_report,
        initial_state,
    )
    return {
        "run_id": initial_state['run_id'],
        "status": "queued",
    }

 
# get report of the job id
@app.get("/get_report/{run_id}")
def get_report_endpoint(
    request: Request,
    run_id: UUID,
):
    result = fetch_report(str(run_id))

    if result is None:
        raise HTTPException(status_code=404, detail="Report run was not found")

    if result["status"] == "completed":
        if result["report"]:
            return {
                "status": "completed",
                "report": result["report"],
            }

        return {
            "status": "failed",
            "error": "The report completed without any report content.",
        }

    if result["status"] == "failed":
        return {
            "status": "failed",
            "error": result["error_message"]
            or "The report could not be generated.",
        }

    return {"status": "pending"}


