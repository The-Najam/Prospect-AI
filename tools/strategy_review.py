from groq import Groq
from config.settings import setting
from models.research_tool_schema import offer_refine, offer_tool_input
import json
from models.workflow_state import state
from config.logger import logger

def offerrefine(strategy_result):

    prompt = """ Act as an expert Offer Refiner. Your job is to improve the wording, clarity, framing, and persuasive strength
    of the offer using ONLY the information provided in the Strategy Result.

    You are NOT an offer creator.
    You must preserve the factual and semantic boundaries of the supplied strategy.

    ## CORE PRINCIPLE ##

    Preserve meaning, improve expression.
    You may:
    - Rewrite wording.
    - Improve clarity.
    - Improve conversational flow.
    - Strengthen framing.
    - Make the offer more concise.
    - Make the value proposition more compelling.
    - Reorganize information when useful.
    - Naturally rephrase the proof and low-risk mechanism.
    - Choose which supported elements to emphasize.

    You must NOT ADD:
    -  new facts.
    -  new claims.
    -  new services.
    -  new deliverables.
    -  new mechanisms.
    -  new features.
    -  guarantees.
    -  audits, trials, pilots, consultations, or implementation steps.
    -  numbers, percentages, timeframes, or metrics.
    -  customer results.
    -  business outcomes not explicitly supported.
    -  sender credentials or experience.
    - Infer unstated problems or consequences.
    - Turn possibilities into facts.
    - Expand the scope of the existing offer.

    ## INPUT ##
    The user will provide a Strategy Result containing:
    - pain
    - problem
    - desirable_outcome
    - proof
    - low_risk
    - value
    Use only these supplied facts and claims.

    ## FIELD-SPECIFIC RULES ##

    ### problem

    You may rewrite the problem for clarity or stronger framing.
    You must preserve:
    - What problem is being described.
    - The certainty level of the problem.
    - Its factual scope.
    Do not introduce a more specific problem unless it is explicitly supported.

    ### desirable_outcome
    You may make the desired outcome clearer or more compelling.
    You must not introduce:
    - New business outcomes.
    - New metrics.
    - New performance claims.
    - New customer outcomes.

    ### proof
    You may naturally rephrase the supplied proof.
    You must preserve the underlying claim.

    Do not add:
    - Customer counts.
    - Case studies.
    - Percentages.
    - Results.
    - Credentials.
    - Experience.
    - Testimonials.

    ### low_risk
    You may improve the wording of the supplied low-risk mechanism.
    You must preserve:
    - The mechanism.
    - The scope.
    - The level of commitment.
    Do not introduce:
    - Free work.
    - Trials.
    - Audits.
    - Pilots.
    - Guarantees.
    - New deliverables.
    - New implementation steps.

    ### value
    You may make the supplied value proposition clearer and more persuasive.
    Do not introduce additional benefits or outcomes.

    ## SEMANTIC BOUNDARY RULE ##
    A rewritten statement is valid only if it means substantially the same thing
    as the original statement.
    Ask internally:
    "Did I merely express the supplied idea better,
    or did I add something that was not there?"
    If the rewrite adds information, remove that information.

    When the supplied information is weak or incomplete, do NOT fill the gaps
    with assumptions or general industry knowledge.

    Weak input must produce a constrained offer, not an invented offer.

    ## EVIDENCE RULE ##

    General knowledge is NOT evidence.
    A statement being generally true in the industry does not make it valid
    for this prospect.
    Only information explicitly supplied in the Strategy Result may be used.

    ## OUTPUT ##
    Return the output in JSON format:

    {
        "refine_offer": "string"
    }

    The refine_offer should contain the refined offer using only supported
    information from the Strategy Result.

    If the supplied strategy does not contain enough information to produce
    a meaningful refined offer, return the schema-defined empty value.

    Never compensate for missing information by inventing information.
    """
    print(type(strategy_result))


    client = Groq(api_key=setting.GROQ_API_KEY)

    chat_completions = client.chat.completions.create(
        model=setting.model,
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

    state.total_token_used += chat_completions.usage.total_tokens
    state.input_tokens += chat_completions.usage.prompt_tokens
    state.output_tokens += chat_completions.usage.completion_tokens
    response = chat_completions.choices[0].message.content
    data = json.loads(response)
    result = offer_refine(**data)
    print(result)
    logger.info("OFFER REFINED SUCCESSFULLY!")

    return(result)



if __name__ == "__main__":
    data =      result = {
  "qualification": "strong",
  "opportunity": {
    "pain": [
      "The company recently launched an online ordering system.",
      "Customers can now place orders through the company's website."
    ],
    "fit": "strong",
    "score": 8
  },
  "offer": {
    "problem": "The online ordering experience may need improvement.",
    "desirable_outcome": "A clearer and easier online ordering experience.",
    "proof": "We help businesses improve online customer experiences.",
    "low_risk": "Start with a small engagement focused on the current ordering experience.",
    "value": "A simpler online ordering experience."
  },
  "reason": {
    "reason": [
      "The company has recently introduced online ordering.",
      "The new ordering experience creates a relevant opportunity for improvement."
    ]
  },
  "angle": {
    "hooks": [
      "New online ordering system",
      "Online customer experience"
    ],
    "angle": "Improve the online ordering experience after the recent launch.",
    "cta": "Open to hearing how?"
  },
  "channel": "linkedin"
}
  


    result = {
        "pain" : data["opportunity"]["pain"],
        "problem" : data["offer"]["problem"],
        "desirable_outcome" : data["offer"]["desirable_outcome"],
        "proof" : data["offer"]["proof"],
        "low_risk" : data["offer"]["low_risk"],
        "value" : data["offer"]["value"],
        "service": "UX design and improvement for online ordering experiences",
    }

    strategy_result = offer_tool_input(**result)
    print(type(strategy_result))
    strategy_result = strategy_result.model_dump_json()
    offerrefine(strategy_result)
