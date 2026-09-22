from models.strategy_schema import Strategy_result
from config.settings import setting
from config.logger import logger
from research.data_cleaner import clean_html
from research.data_extraction import main
from research.research_analyzer import analyzer
from tools.additional_research import missing_info_research
from groq import Groq
import json
import asyncio



def strategy_reasoning(strategy_input):
    print(type(strategy_input))
    prompt = """
    Act as an expert in prospect qualification strategy and offer creation.

    Review the provided research and determine whether any critical information is missing that could materially affect the quality of the qualification strategy or offer.

    If critical information is missing, use the additional_research tool to obtain it.

    ## RULES ##
    Use additional_research only when the missing information could materially improve the strategy or offer.
    Do not use additional research for minor or non-critical gaps.
    Clearly identify what information is missing when calling the tool.
    Use the available research when sufficient information exists.

    """ 
    tools = [
        {
            "type": "function",
            "function": {
                "name": "additional_research",
                "description": "Do Additional Research for Missing field to Improve Strategy and Offer Creation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "CompanyData": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string"
                                },
                                "about": {
                                    "type": "string"
                                },
                                "location": {
                                    "type": "string"
                                },
                                "industry": {
                                    "type": "string"
                                },
                                "company_size": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "name",
                                "about",
                                "location",
                                "industry",
                                "company_size"
                            ]
                        },

                        "services": {
                            "type": "object",
                            "properties": {
                                "services": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string"
                                            },
                                            "description": {
                                                "type": "string"
                                            },
                                            "Pricing": {
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "name",
                                            "description",
                                            "Pricing"
                                        ]
                                    }
                                }
                            },
                            "required": [
                                "services"
                            ]
                        },

                        "icp": {
                            "type": "object",
                            "properties": {
                                "Type": {
                                    "type": "string"
                                },
                                "location": {
                                    "type": "string"
                                },
                                "Needs": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "Buying_behaviour": {
                                    "type": "string"
                                },
                                "objections": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "Type",
                                "location",
                                "Needs",
                                "Buying_behaviour",
                                "objections"
                            ]
                        },

                        "opportunties": {
                            "type": "object",
                            "properties": {
                                "Pain_points": {
                                    "type": "array",
                                    "items" : {
                                        "type" : "string"
                                    }
                                }
                            },
                            "required": [
                                "Pain_points"
                            ]
                        }
                    },

                    "required": [
                        "CompanyData",
                        "services",
                        "icp",
                        "opportunties"
                    ]
                }
            }
        }
    ]
    try:
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
                    "content" : strategy_input
                }

            ],
            tools=tools
        )

        if chat_completions.choices[0].message.tool_calls[0]:
            logger.info("Tool Called!")
            tool = chat_completions.choices[0].message.tool_calls[0]
            arguments = json.loads(tool.function.arguments)
            tool_id = tool.id
            logger.info("Arguments Extracted")
            tool_arguments = research_result.model_dump(
                include={
                    "CompanyData",
                    "services",
                    "icp",
                    "opportunties"
                }
            )
            extra_research = missing_info_research(arguments)
            tool_result = {
                    "role" : "tool",
                    "tool_call_id" : tool_id,
                    "content" : extra_research
            }
            print("TYPE OF STRATEGY INPUT", type(strategy_input))
            result = strategy_agent(strategy_input)
            print(result)
            logger.info("Strategy Created Successfully!")
            return result
        else:
            result = strategy_agent(strategy_input)
            print(result)
            return result
    except Exception as e:
        logger.info("Can't Create Strategy", e)



def strategy_agent(strategy_input):
    # strategy_input = json.dumps(strategy_input)
    print("TYPE" , type(strategy_input))
    system_prompt = """
    ## ROLE ##
    Act as an expert in Prospects Qualification Startegy and offer Creation. You know how to find the right opportunites which need to fix urgently.
    
    For this given ideal client profile, I want you to do create a powerfull strategy for outreaching to prospects and provide the following.
    
    ## OUTPUT ##
    Return the result as valid JSON matching the format below
    
    {
    "qualification": strong,
    "opportunity": {
        "pain": [string],
        "fit": string,
        "urgency": string,
        "Timing": string,
        "score": 8
    },
    "offer": {
        "problem": string,
        "desirable_outcome": string,
        "proof": string,
        "low_risk": string,
        "value": string
    },
    "reason": {
        "reason": [string]
    },
    "angle": {
        "hooks": [string],
        "angle": string,
        "cta": string
    }
    }

    ## FIELD DEFINATION
    qualification : You must rank the prospect qualification among this list of qualification: 'strong' | 'medium' | 'weak'
    opportunity :
           - pain : Take the pain points identified by the Research Agent and select only those that represent a meaningful sales opportunity.
           - fit : does the prospects is right match for services
           - urgency : how urgently problem need to fix
           - timing : does this is the right time to reach out
           - score : score should reflect: service fit, severity of pain, urgency, timing, evidence supporting the opportunity and based on it rank a prospect which matches the most out of 10
    offer:
           - problem : what problem you're solving
           - desirable_outcome : what outcome prospects get from the services
           - proof : This will be provided by user so you must use that
           - low_risk : what the lowest possible risk you can provide to prospect
           - value : after buying services what change or difference it will make.
    
    reason: The offer you recommended, give the reason why you make this offer and what's the purpose behind it

    angle: 
           - hooks : List down the top level suggestions of hooks which grab the attention
           - angle : mention the best angle which can be use for prospect
           - cta : mention the cta which makes prospect to take action
    
    ## RULES ##
    1. EVIDENCE BOUNDARY
    - Build the entire strategy exclusively from the Research Result and the user's explicitly provided information.
    - Do not introduce facts, claims, problems, motivations, intent, urgency, timing, outcomes, capabilities, or business conditions that are not supported by those sources.
    - If required information is not supported by the available evidence, return the required field as `""`, `[]`, or the schema-defined empty value.
    - Never fill missing information with assumptions, industry knowledge, probabilities, or what would "normally" be true.

    2. FACT VS INFERENCE
    - Treat information explicitly stated in the Research Result as FACT.
    - Strategic reasoning may contain INFERENCES only when they are directly and logically supported by one or more specific research facts.
    - Never present an inference as a confirmed fact.
    - When making an inference, clearly distinguish the observed evidence from the interpretation.
    - Do not chain multiple assumptions together to produce a conclusion.
    - If an inference requires an unsupported assumption, do not make the inference.

    3. PAIN POINT CONSTRAINT
    - Use only pain points explicitly identified in the Research Result.
    - You may shorten, combine, or rephrase an existing pain point without changing its meaning.
    - You must not add, expand, diagnose, or derive a new pain point from an existing one.
    - Do not infer the underlying cause of a documented pain unless the Research Result explicitly establishes that cause.
    - If no relevant pain point is supported, return `[]`.

    4. PROSPECT INTENT
    - Never assume the prospect wants, needs, is interested in, or is considering the user's service unless the Research Result explicitly provides evidence of such intent.
    - A business problem, pain point, opportunity, or missing capability does NOT by itself prove buying intent.
    - If prospect intent is not explicitly supported, do not describe it as confirmed intent.

    5. PROSPECT FIT
    - Provide qualification reasoning using only observable evidence from the Research Result.
    - Every positive fit claim must be traceable to specific research evidence.
    - Do not convert "could benefit from" into "needs."
    - Do not convert "matches the target market" into "is likely to buy."
    - If evidence is insufficient to establish fit, lower the score or return the schema-defined uncertain/empty value rather than inventing justification.

    6. URGENCY
    - Do not assign urgency based solely on the existence or severity of a problem.
    - "High", "Medium", or equivalent urgency must be supported by explicit evidence of time pressure, business impact, an active initiative, deadline, escalation, or another concrete urgency signal in the Research Result.
    - If no urgency signal exists, return `""` or the schema-defined unknown value.
    - Never manufacture urgency to strengthen an offer.

    7. TIMING
    - Timing must be based only on explicit timing signals in the Research Result.
    - Valid timing evidence may include stated deadlines, launches, hiring plans, active projects, upcoming events, expansion plans, or other explicitly documented time-bound signals.
    - Do not infer "Immediate", "Now", "Soon", or similar timing from pain severity, fit, or urgency alone.
    - If no timing signal exists, return `""`.

    8. QUALIFICATION SCORING
    - Every qualification score must be justified using evidence available in the Research Result.
    - Do not increase a score because an assumption makes the prospect appear more attractive.
    - Do not use the score itself as evidence.
    - If evidence is weak or missing, reflect that uncertainty in the score.

    9. OFFER CONSTRAINT
    - Recommend an offer only from problems, needs, opportunities, capabilities, and constraints supported by the Research Result and the user's explicitly provided service information.
    - Do not invent services, deliverables, mechanisms, features, guarantees, audits, pilots, trials, implementation steps, or other components that the user did not provide.
    - Do not expand a low-risk offer beyond the mechanisms explicitly provided by the user.
    - If no evidence supports a meaningful offer, return the schema-defined empty value.

    10. OFFER OUTCOME CLAIMS
        - Never promise or state unsupported outcomes such as increased revenue, more leads, higher conversion, reduced costs, measurable ROI, saved time, or guaranteed results.
        - An outcome may be mentioned only when it is explicitly supported by the Research Result or explicitly provided by the user.
        - Otherwise, describe the proposed value as a potential objective or intended benefit, not an established result.
        - Never use absolute, guaranteed, or certainty-based language without evidence.

    11. LOW-RISK / PROOF CONSTRAINT
        - Proof and low-risk are direct user inputs and must be preserved exactly as provided, regardless of qualification or opportunity strength. They must not be generated, modified, or omitted unless the user did not provide them.
        - If no valid proof or low-risk mechanism exists, return `""` or the schema-defined empty value.
        - Never invent testimonials, case studies, previous results, guarantees, pilots, audits, free trials, or other trust mechanisms.

    12. HOOK CONSTRAINT
        - Hooks must be created only from facts, pain points, opportunities, or observations supported by the Research Result.
        - Do not introduce unsupported claims about traffic, competitors, advertising spend, customer behavior, revenue, missed opportunities, growth, urgency, or business performance.
        - A hook may frame an existing fact creatively, but it must not change or exaggerate its factual meaning.
        - Do not use a stronger claim simply because it produces a more compelling hook.

    13. STRATEGIC REASONING
        - For every recommendation requiring reasoning, explain why it follows from the available evidence.
        - Reasoning must connect:
        Research Evidence → Interpretation → Recommendation.
        - Do not introduce new facts between these stages.

    14. EVIDENCE TRACEABILITY
        - Every factual claim, qualification factor, urgency signal, timing signal, pain point, and strategic recommendation must be traceable to the Research Result or explicit user input.
        - If a claim cannot be traced to evidence, remove it or return the appropriate empty value.
        - Do not use external knowledge to strengthen weak evidence.

    15. UNCERTAINTY HANDLING
        - Missing evidence must remain missing.
        - Do not convert uncertainty into probability, probability into confidence, or confidence into fact.
        - Prefer an empty field over an unsupported conclusion.
        - A weaker but evidence-backed recommendation is always preferable to a stronger recommendation based on assumptions.

    16. OUTPUT CONSTRAINT
        - Return only the structured result defined by the output schema.
        - Do not add explanations, commentary, disclaimers, or text outside the structure.
        - Follow the schema exactly, including required field types and empty-value conventions.
        
    17. PROSPECT-SCOPE CONSTRAINT

    - All pain points, problems, opportunities, fit, urgency, and timing must refer to the prospect company itself.
    - Do not treat the prospect's customers, target audience, ICP, market, or clients as the prospect.
    - A need or pain described for the prospect's customers does not count as a pain of the prospect.
    - Do not recommend an offer based solely on a problem the prospect solves for its own customers.
    - Only select an opportunity when there is evidence that the prospect itself experiences, needs, lacks, or could directly benefit from the user's service.
    
    18. PROSPECT OWNERSHIP OF PAIN

    - A pain point listed in the Research Result is not automatically a pain experienced by the prospect.
    - Before selecting a pain as an opportunity, verify that the Research Result contains evidence connecting that pain specifically to the prospect.
    - Pain points describing the prospect's ICP, customers, target audience, market, or services they provide must not be treated as the prospect's own pain.
    - If the Research Result only states that the prospect's customers have a problem, that problem cannot be used as the prospect's opportunity.
    - If the prospect already provides the user's service, do not assume the prospect needs the same service for its own business.
    - The fact that a service is listed in the prospect's services does not prove that the prospect itself needs that service.

    SERVICE CONFLICT

    - If the prospect already offers the same or substantially similar service as the user's service, treat this as a negative fit signal.
    - Do not recommend selling that same service to the prospect unless the Research Result contains explicit evidence that the prospect itself has a need for it.
    - Do not infer that the prospect's own website, marketing, branding, SEO, or other business assets are deficient merely because the prospect offers those services to customers.
    """
    try:
        client = Groq(
            api_key=setting.GROQ_API_KEY
        )

        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role" : "system",
                    "content" : system_prompt
                },
                {
                    "role" : "user",
                    "content" : strategy_input
                }
            ],
            response_format={
                "type":"json_object",
                "json_object":{
                    "name":"Strategy_result",
                    "strict":True,
                    "schema": Strategy_result.model_json_schema()
                }
            }
        )
        response = chat_completion.choices[0].message.content
        result = Strategy_result(**json.loads(response))
        logger.info("Strategy Created Sucessfully")
        return result
    except Exception as e:
        logger.error("Strategy Creation Failed", e)



if __name__ == "__main__":
    page_content = asyncio.run(main())
    content = clean_html(page_content)
    research_result = analyzer(content)
    print(type(research_result))
    result = research_result.model_dump()
    # service = input("Enter the services you're offering")
    # proof = input("Enter the proof you have?")
    # low_risk = input("Enter the Low Risk mechanism")
    result['user_service'] = "web designinh"
    result['user_proof'] = "7+ years of experience"
    result['Low-risk-mechanism'] = "free demo"
    strategy_input = json.dumps(result)
    strategy_result = strategy_reasoning(strategy_input)