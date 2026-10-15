from research.research_analyzer import research_agent_workflow
from research.data_cleaner import clean_html
from research.data_extraction import fetch_all, input_links,fetch_homepage, normalize_deduplicate_links, url_classification
from strategy.strategy_agent import strategy_agent_workflow
from outreach.ai_copywriter import outreach_agent_workflow
from outreach.final_report import report, partial_report, research_report
from models.workflow_state import WorkflowState
from config.logger import logger
from config.settings import setting
from datetime import datetime, timezone
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from database.database import create_dbconnection, insert_data, update_data, updata_data_fail
import uuid
import asyncio
import json
import selectors
from langsmith import Client


# Content Routing
def content_routing(state:WorkflowState):
    if state["content_status"] == "success":
        return "success"

    if state["cleaned_content_attempts"] < state["max_attempts"]:
        return "retry"

    return "failed"
    



# taking input of data
def input_data(research_result):
    research_result.user_service = input("Enter The Service You're Offering")
    research_result.user_low_risk = input("Enter Free Risk Offer You can Provide")
    research_result.user_proof = input("Enter the proof : ")
    channel = input("Enter the channel Name : ")
    return research_result,channel


# research route function
def research_route(state:WorkflowState): 
    if state['research_status'] == "success":
        return "success"
    elif state['research_attempts'] < state['max_attempts']:
        return "retry"
    else:
        return "failed"

# strategy route function
def strategy_route(state:WorkflowState):
    if state['strategy_status'] == "success":
        return "success"
    elif state['strategy_attempts'] < state['max_attempts']:
        return "retry"
    else:
        return "failed"

# outreach route function
def outreach_route(state:WorkflowState):
    if state['outreach_status'] == "success":
        return "success"
    elif state['outreach_attempts'] < state['max_attempts']:
        return "retry"
    else:
        return "failed"

# async homepage node
async def get_homepage_node(state: WorkflowState):
    return await asyncio.to_thread(lambda: asyncio.run(fetch_homepage(state)))

# async node for fetching all pages
async def fetch_all_node(state: WorkflowState):
    return await asyncio.to_thread(lambda: asyncio.run(fetch_all(state)))

# getting prospect_url
def get_url_node(state: WorkflowState):
    return {"prospect_url": state["prospect_url"]}

# main workflow
async def workflow(prospect_url: str):
    # generating id
    run_id = str(uuid.uuid4())

    # defining initial state
    initial_state = {
        "prospect_url": prospect_url,
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
    }

    # configuration
    config = {
        "configurable": {
            "thread_id": run_id,
        }
    }

    # defining Graph
    prospect_graph = StateGraph(WorkflowState)
    
    

    # creating Nodes
    nodes = [
        ("get_url", get_url_node),
        ("get_homepage", get_homepage_node),
        ("normalize_deduplicate_links",normalize_deduplicate_links),
        ("url_classification",url_classification),
        ("fetch_all_url",fetch_all_node),
        ("get_clean_content",clean_html),
        ("get_research_result", research_agent_workflow),
        ("get_strategy_result", strategy_agent_workflow),
        ("get_outreach_result", outreach_agent_workflow),
        ("get_final_report", report),
        ("get_research_report", research_report),
        ("get_partial_report", partial_report)
    ]
    for name,func in nodes:
        prospect_graph.add_node(name,func)

    # creating Edges
    prospect_graph.add_edge(START,"get_url")
    prospect_graph.add_edge("get_url","get_homepage")
    prospect_graph.add_edge("get_homepage","normalize_deduplicate_links")
    prospect_graph.add_edge("normalize_deduplicate_links","url_classification")
    prospect_graph.add_edge("url_classification","fetch_all_url")
    prospect_graph.add_edge("fetch_all_url","get_clean_content")
    prospect_graph.add_conditional_edges(
        "get_clean_content",
        content_routing,
        {
            "success":"get_research_result",
            "retry":"get_clean_content",
            "failed":END
        }
    )
    prospect_graph.add_conditional_edges(
        "get_research_result",
        research_route,
        {
            "success":"get_strategy_result",
            "retry" : "get_research_result",
            "failed":"get_research_report"
        }
    )
    prospect_graph.add_conditional_edges(
        "get_strategy_result",
        strategy_route,
        {
            "success":"get_outreach_result",
            "retry":"get_strategy_result",
            "failed":"get_partial_report"
        }
    )
    prospect_graph.add_conditional_edges(
        "get_outreach_result",
        outreach_route,
        {
            "success":"get_final_report",
            "retry":"get_outreach_result",
            "failed":"get_partial_report"
        }
    )
    prospect_graph.add_edge("get_final_report", END)
    prospect_graph.add_edge("get_partial_report", END)
    prospect_graph.add_edge("get_research_report", END)

    # compilation
    connection = f"postgresql://{setting.DB_USER}:{setting.DB_PASSWORD}@localhost:5432/prospect-ai"
    async with AsyncPostgresSaver.from_conn_string(connection) as checkpointer:
        await checkpointer.setup()
        prospect_workflow = prospect_graph.compile(checkpointer=checkpointer)
        try:
            result = await prospect_workflow.ainvoke(initial_state, config=config)
            snapshot = await prospect_workflow.aget_state(config)
            return {
                "run_id": run_id,
                "input_url": prospect_url,
                "state": snapshot.values,
                "result": result,
            }
        except Exception as exc:
            logger.exception("Workflow execution failed")
            return {
                "run_id": run_id,
                "input_url": prospect_url,
                "state": initial_state,
                "result": {
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            }
        
# For testing Concurrent Users
async def test_concurrent_runs():
    first_url = "https://example.com/"
    second_url = "https://example.com/"

    first_result, second_result = await asyncio.gather(
        workflow(first_url),
        workflow(second_url),
    )

    assert first_result["run_id"] != second_result["run_id"]

    assert first_result["input_url"] == first_url
    assert second_result["input_url"] == second_url

    assert first_result["state"]["prospect_url"] == first_url
    assert second_result["state"]["prospect_url"] == second_url

    assert "error_type" not in first_result["result"]
    assert "error_type" not in second_result["result"]

    print("Concurrent state-isolation test passed")
    print(f"Run 1 thread ID: {first_result['run_id']}")
    print(f"Run 2 thread ID: {second_result['run_id']}")


if __name__ == "__main__":
    # result = asyncio.run(
    #     workflow(),
    #     loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()),
    # )
    # if result is not None:
    #     print("RESULT : \n\n\n",result["final_report"])

    asyncio.run(
        test_concurrent_runs(),
        loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()),
    )



