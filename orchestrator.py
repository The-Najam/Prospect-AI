from research.research_analyzer import analyzer
from research.data_cleaner import clean_html
from research.data_extraction import fetch_all, input_links,fetch_homepage, normalize_deduplicate_links, url_classification
from strategy.strategy_agent import strategy_agent
from outreach.ai_copywriter import outreach_message
from outreach.final_report import report
from models.workflow_state import state
from config.logger import logger
from datetime import datetime, timezone
from database.database import create_dbconnection, insert_data, update_data, updata_data_fail
import uuid
import asyncio
import json


def start_run(url):
    run_id = uuid.uuid4()
    started_at = datetime.now(timezone.utc)
    status = 'running'
    conn, cur = create_dbconnection()
    insert_data(conn,cur,url,run_id,started_at,status)
    return started_at, run_id

    

def complete_run(run_id,completed_at,latency, estimated_cost):
    try:
        conn, cur = create_dbconnection()
        update_data(conn,cur,run_id,completed_at,latency,estimated_cost)
        logger.info("DataBase Updated Successfully")
    except Exception as e:
        logger.error("Failed To Update Database", e)


def fail_run(run_id,error_type,retry_count,estimated_cost,latency):
    completed_at = datetime.now(timezone.utc)
    conn, cur = create_dbconnection()
    updata_data_fail(conn,cur, run_id,completed_at,latency,estimated_cost,error_type,retry_count)






def input_data(research_result):
    research_result.user_service = "Graphic Design"
    research_result.user_low_risk = "Free Designs"
    research_result.user_proof = "7 years of experience"
    channel = "instagram"


    return research_result,channel


def data_route(state):
    if state.Data_Extraction:
        return "research"
    return "retry"


def research_route(state):
    if state.research_result:
        return "strategy"
    return "retry"

def strategy_route(state):
    if state.strategy_result:
        return "outreach"
    return "retry"

def outreach_route(state):
    if state.outreach_result:
        return "completed"
    return "retry"


def research_step():
    try:
        research_result = analyzer(state.Data_Extraction[:2])
        print("Current Status : ", state.status)
        print("Current Step : ", state.current_step)
        next_step = research_route(state)
        print("RESEARCH RETURNED:", research_result)
        return research_result, next_step
    except Exception:
        logger.exception("Failed To generate Research ! ")
        raise


def strategy_step():
    try:
        strategy_result = strategy_agent(json.dumps(state.research_result.model_dump()))
        state.current_step = "Strategy"
        print("Current Status : ", state.status)
        print("Current Step : ", state.current_step)
        next_step = strategy_route(state)
        #print("STRATEGY RETURNED:", strategy_result)

        return strategy_result, next_step

    except Exception as e:
        logger.exception("Failed To generate Outreach ! ",e)
        raise




def outreach_step():
    try:
        strategy_result = json.dumps(state.strategy_result.model_dump())
        outreach_result = outreach_message(strategy_result) 
        Final_report = report(state.research_result, state.strategy_result, outreach_result)
        state.current_step = "outreach"
        print("Current Status : ", state.status)
        print("Current Step : ", state.current_step)
        next_step = outreach_route(state)
        # print("OUTREACH RETURNED:", outreach_result)
        # print("Final Report : ", Final_report)
        return outreach_result, Final_report, next_step
    except Exception:
        logger.exception("Failed To generate Outreach ! ")
        raise



def workflow(retry_count, max_retry, url):
    state.status = "running"
    url = input_links()
    started_at , run_id = start_run(url)
    page_content, links  = asyncio.run(fetch_homepage(url))
    urls = normalize_deduplicate_links(links,url)
    selected_pages_url = url_classification(urls)
    selected_pages_url.append({"url":url, "page_type":"Home"})
    page_content = asyncio.run(fetch_all(selected_pages_url))
    state.Data_Extraction = clean_html(page_content)
    


    next_step = data_route(state)
    if next_step == "research":
        state.research_result, next_step = research_step()
        print("OUTER RESEARCH : ", state.research_result)
    elif next_step == "retry":
        while True:
            if retry_count < max_retry:
                state.research_result, next_step = research_step()
                retry_count += 1
                if next_step == "strategy":
                    retry_count = 0
                    break
            else:
                error_type = 'research'
                estimated_cost = (state.input_tokens / (1000000 * 0.15)) + (state.output_tokens / (1000000 * 0.60))
                fail_run(run_id,error_type,retry_count,estimated_cost,latency)
                return None

    
    research_result, state.channel = input_data(state.research_result)
    next_step = research_route(state)
    if next_step == "strategy":
        state.strategy_result, next_step = strategy_step()
        state.strategy_result.channel = state.channel
    elif next_step == "retry":
            while True:
                if retry_count < max_retry:
                    state.strategy_result, next_step= strategy_step()
                    retry_count += 1
                    if next_step == "outreach":
                        retry_count = 0
                        break
                else:
                    error_type = 'strategy'
                    estimated_cost = (state.input_tokens / (1000000 * 0.15)) + (state.output_tokens / (1000000 * 0.60))
                    fail_run(run_id,error_type,retry_count,estimated_cost,latency)
                    return None

    

    next_step = strategy_route(state)
    if next_step == "outreach":
        state.outreach_result, state.Final_report, next_step = outreach_step()
        print("OUTREACH : ",state.outreach_result)
    elif next_step == "retry":
        state.status = "retry"
        while True:
            if retry_count < max_retry:
                state.outreach_result, state.Final_report, next_step = outreach_step()
                retry_count += 1
                if next_step == "completed":
                    retry_count = 0
                    break
            else:
                logger.error("Outreac Generation Failled")
                error_type = 'outreach'
                estimated_cost = (state.input_tokens / (1000000 * 0.15)) + (state.output_tokens / (1000000 * 0.60))
                fail_run(run_id,error_type,retry_count,estimated_cost,latency)
                return None
        

    state.current_step = "completed"
    state.status= "completed"

    print("Current Status : ", state.status)
    print("Current Step : ", state.current_step)
    completed_at = datetime.now(timezone.utc)
    latency = completed_at.timestamp() - started_at.timestamp()
    print("TOTAL TOKEN USED : ",state.total_token_used)
    print("TOTAL INPUT TOKENS : ", state.input_tokens)
    print("TOTAL OUTPUT TOKENS : ", state.output_tokens)
    estimated_cost = (state.input_tokens / (1000000 * 0.15)) + (state.output_tokens / (1000000 * 0.60))
    complete_run(run_id,completed_at,latency,estimated_cost)
    return state.Final_report


if __name__ == "__main__":
    retry_count = 0
    max_retry = 3
    url = input_links()

    workflow(retry_count,max_retry,url)



