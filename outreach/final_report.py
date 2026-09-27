from research.research_analyzer import analyzer, clean_html, fetch_all
from strategy.strategy_agent import strategy_agent
from outreach.ai_copywriter import outreach_message
import asyncio
import json

def report(research_result,strategy_result,outreach):
    return {
        "Company_Overview" : {
            "name" : research_result.CompanyData.name,
            "about" : research_result.CompanyData.about,
            "location" : research_result.CompanyData.location,
            "company_size" : research_result.CompanyData.Company_size,
        },
        "Business_Analysis" : {
            "services" : research_result.services,
            "Type" : research_result.icp.Type,
            "Location" : research_result.icp.location,
            "Needs" : research_result.icp.Needs,
            "Buying_Behaviour" : research_result.icp.Buying_behavior,
            "Objections" : research_result.icp.Objections, 
        },
        "Opportunities":{
            "Pain_Points" : research_result.opportunties.Pain_points,
            "fit" : strategy_result.opportunity.fit,
            "urgency": strategy_result.opportunity.urgency,
            "Timing" :  strategy_result.opportunity.Timing,
        },
        "Qualification":{
            "Qualification" : strategy_result.qualification,
            "Score" : strategy_result.opportunity.score,
        },
        "Recommended Offer": {
            "problem" : strategy_result.offer.problem,
            "Desirable_outcome": strategy_result.offer.desirable_outcome,
            "proof" : strategy_result.offer.proof,
            "low_risk" : strategy_result.offer.low_risk,
            "Value" : strategy_result.offer.value,
        },

        "Outreach_Package" : {
            "channel": outreach.channel,
            "message" : outreach.outreach_msg
        }

    }



if __name__ == "__main__":
    raw_data = asyncio.run(main())
    clean_content = clean_html(raw_data)
    research_result = analyzer(clean_content)
    result = research_result.model_dump()
    service = "web designing"
    proof = "6+ years of experience"
    low_risk = "Free Demo"
    result['user_service'] = service
    result['user_proof'] = proof
    result['Low-risk-mechanism'] = low_risk
    strategy_input = json.dumps(result)
    strategy_result = strategy_agent(strategy_input)
    result_strategy = strategy_result.model_dump()
    result_strategy['channel'] = "instagram"
    outreach_input = json.dumps(result_strategy)
    outreach_result = outreach_message(outreach_input)
    Final_report = report(research_result, strategy_result, outreach_result)
    print(Final_report)
    