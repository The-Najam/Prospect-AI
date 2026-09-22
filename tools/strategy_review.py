from groq import Groq
from config.settings import setting
from models.research_tool_schema import offer_refine, offer_tool_input
import json
from config.logger import logger

def offerrefine(strategy_result):

    prompt = """
    Act as an expert Offer Strategist. Specialize in creating the killer and irresistable offer.

    ## OUTPUT ##

    Return the Output in JSON format below

    {
        "refine_offer" : str
    }


    ## RULES ##
    1. Use the provided pain, urgency , problem, outcome, proof, low_risk, service to create the offer.
    2. You must create the offer based on avialable data
    3. Do not invent, assume, or hallucinate information.
    4. Include only information supported by the strategy.
    5. Do not invent services, deliverables, mechanisms, features, guarantees, audits, pilots, trials, implementation steps, or other components that the user did not provide.
    6. Do not expand a low-risk offer beyond the mechanisms explicitly provided by the user.
    7. If no evidence supports a meaningful offer, return the schema-defined empty value.
    8. Never promise or state unsupported outcomes such as increased revenue, more leads, higher conversion, reduced costs, measurable ROI, saved time, or guaranteed results.
    9. An outcome may be mentioned only when it is explicitly supported by the strategy result or explicitly provided by the user.
    10. You must use the proof and low_risk provided by strategy result and must be preserved exactly as provided


    """
    print(type(strategy_result))


    client = Groq(
        api_key=setting.GROQ_API_KEY
    )

    chat_completions = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role" : "system",
                "content" : prompt
            },
            {
                "role" : "user",
                "content" : strategy_result
            }
        ],
        response_format = {
            "type" : "json_object",
            "json_object" : {
                "name" : "offer_refine",
                "strict" : True,
                "schema" : offer_refine.model_json_schema()
            }
        }
    )


    response = chat_completions.choices[0].message.content
    data = json.loads(response)
    result = offer_refine(**data)
    print(result)

    logger.info("OFFER REFINED SUCCESSFULLY!")

    return(result)



if __name__ == "__main__":
    data =  {
     "qualification": "weak",
     "opportunity": {
       "pain": [
         "They have some problems",
         "Sales could be better",
         "Things are not always efficient"
       ],
       "fit": "Maybe a good fit because they are a company.",
       "urgency": "Not sure, probably medium.",
       "Timing": "Maybe sometime soon.",
       "score": 35
     },
     "offer": {
       "problem": "They have business problems and need help improving things.",
       "desirable_outcome": "They want to grow their business and get better results.",
       "proof": "We have experience helping companies.",
       "low_risk": "We can try it and see what happens.",
       "value": "It could save time and make more money."
     },
     "reason": {
       "reason": [
         "They seem like they might need this.",
         "Their business could probably improve.",
         "There may be an opportunity here."
       ]
     },
     "angle": {
       "hooks": [
         "Want to improve your business?",
         "We can help you grow.",
         "Are you looking for better results?"
       ],
       "angle": "Offer them a solution that can help their business.",
       "cta": "Let me know if you are interested."
     },
     "channel": "email"
   }



    result = {
        "pain" : data["opportunity"]["pain"],
        "urgency" : data["opportunity"]["urgency"],
        "problem" : data["offer"]["problem"],
        "desirable_outcome" : data["offer"]["desirable_outcome"],
        "proof" : data["offer"]["proof"],
        "low_risk" : data["offer"]["low_risk"],
        "value" : data["offer"]["value"]
    }

    strategy_result = offer_tool_input(**result)
    print(type(strategy_result))
    strategy_result = strategy_result.model_dump_json()
    offerrefine(strategy_result)
