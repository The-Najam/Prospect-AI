from research.research_analyzer import research_agent_workflow, clean_html, fetch_all, user_data, url_classification,fetch_homepage,normalize_deduplicate_links
from strategy.strategy_agent import strategy_agent, strategy_agent_workflow
from outreach.ai_copywriter import outreach_agent_workflow, outreach_message
import asyncio
import json

def _field(obj, name, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _dump(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return obj


def report(research_result, strategy_result, outreach):
    research = _dump(research_result)
    company = _field(research, "company", {}) or {}
    offer = _field(strategy_result, "offer", {}) or {}
    angle = _field(strategy_result, "angle", {}) or {}
    reasoning = _field(strategy_result, "reasoning", {}) or {}

    return {
        "Company_Overview": {
            "name": _field(company, "name"),
            "about": _field(company, "about"),
            "industry": _field(company, "industry"),
            "locations": _field(company, "locations", []),
            "contact_paths": _field(company, "contact_paths", []),
        },
        "Research": {
            "services": _field(research, "services", []),
            "business_type": _field(research, "business_type"),
            "people": _field(research, "people", []),
        },
        "Strategy": {
            "qualification": _field(strategy_result, "qualification"),
            "fit": _field(strategy_result, "fit"),
            "fit_reasons": _field(strategy_result, "fit_reasons", []),
            "reasoning": _field(reasoning, "reason", []),
        },
        "Recommended_Offer": {
            "problem": _field(offer, "problem"),
            "desirable_outcome": _field(offer, "desirable_outcome"),
            "proof": _field(offer, "proof"),
            "low_risk": _field(offer, "low_risk"),
            "value": _field(offer, "value"),
        },
        "Outreach_Angle": {
            "hooks": _field(angle, "hooks", []),
            "angle": _field(angle, "angle"),
            "cta": _field(angle, "cta"),
        },
        "Outreach_Package": {
            "channel": _field(outreach, "channel"),
            "message": _field(outreach, "outreach_msg"),
        },
    }




if __name__ == "__main__":
    user_service, low_risk, proof = user_data()
    url = "https://www.vistadentalimplants.com/"

    page_content, links  = asyncio.run(fetch_homepage(url))
    urls = normalize_deduplicate_links(links,url)
    selected_pages_url = url_classification(urls)
    selected_pages_url.append({"url":url, "page_type":"Home"})
    page_content = asyncio.run(fetch_all(selected_pages_url))
    content = clean_html(page_content)
    content = content.model_dump()
    research_result = research_agent_workflow(content,user_service)
    research_result.user_service = user_service
    research_result.user_proof = proof
    research_result.user_low_risk = low_risk
    strategy_input = research_result.model_dump()
    strategy_result = strategy_agent_workflow(strategy_input)
    result_strategy = strategy_result.model_dump()
    result_strategy["channel"] = "instagram"
    result_strategy["user_service"] = user_service
    outreach_result = outreach_agent_workflow(result_strategy)
    Final_report = report(research_result, strategy_result, outreach_result)
    print(Final_report)
