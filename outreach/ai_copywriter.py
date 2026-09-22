from config.settings import setting
from config.logger import logger
from groq import Groq
from research.research_analyzer import analyzer, clean_html, main
from strategy.strategy_agent import strategy_agent
from models.outreach_schema import Outreach_Message
from models.research_tool_schema import offer_tool_input
from tools.strategy_review import offerrefine
import asyncio
import json


def review(outreach_input):
    system_prompt = """
    ## ROLE ##
    Act as an expert cold-outreach copywriter specializing in attention-grabbing and persuasive outreach messages.

    You understand sales psychology, persuasion, and effective offer positioning.

    Before writing the outreach message, evaluate the offer in the strategy result. If the offer is weak enough that refining it could materially improve the quality or effectiveness of the outreach, call `offer_refine`.

    ## RULES ##
    - Use `offer_refine` only when the current offer has a meaningful weakness that could materially reduce outreach effectiveness.
    - Do not use `offer_refine` for minor wording improvements, stylistic preferences, or small refinements.
    - If the offer is already strong and usable for outreach, do not call `offer_refine`.
    - When calling `offer_refine`, always provide all required arguments with the relevant values from the strategy result.
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "offerrefine",
                "description": "Refine the strategy result when the current offer is weak.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "qualification": {
                            "type": "string",
                            "enum": [
                                "strong",
                                "medium",
                                "weak"
                            ],
                            "description": "Overall qualification of the opportunity."
                        },
                        "opportunity": {
                            "type": "object",
                            "properties": {
                                "pain": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "Key pains or problems identified."
                                },
                                "fit": {
                                    "type": "string",
                                    "description": "How well the opportunity fits the solution."
                                },
                                "urgency": {
                                    "type": "string",
                                    "description": "How urgent the problem is."
                                },
                                "Timing": {
                                    "type": "string",
                                    "description": "Expected timing for action or purchase."
                                },
                                "score": {
                                    "type": "integer",
                                    "description": "Opportunity score."
                                }
                            },
                            "required": [
                                "pain",
                                "fit",
                                "urgency",
                                "Timing",
                                "score"
                            ]
                        },
                        "offer": {
                            "type": "object",
                            "properties": {
                                "problem": {
                                    "type": "string",
                                    "description": "The specific problem the offer addresses."
                                },
                                "desirable_outcome": {
                                    "type": "string",
                                    "description": "The desired outcome for the prospect."
                                },
                                "proof": {
                                    "type": "string",
                                    "description": "Evidence supporting the offer."
                                },
                                "low_risk": {
                                    "type": "string",
                                    "description": "How the offer reduces perceived risk."
                                },
                                "value": {
                                    "type": "string",
                                    "description": "The value created by the offer."
                                }
                            },
                            "required": [
                                "problem",
                                "desirable_outcome",
                                "proof",
                                "low_risk",
                                "value"
                            ]
                        },
                        "reason": {
                            "type": "object",
                            "properties": {
                                "reason": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "Reasons supporting the strategy recommendation."
                                }
                            },
                            "required": [
                                "reason"
                            ]
                        },
                        "angle": {
                            "type": "object",
                            "properties": {
                                "hooks": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "Potential outreach hooks."
                                },
                                "angle": {
                                    "type": "string",
                                    "description": "The core outreach angle."
                                },
                                "cta": {
                                    "type": "string",
                                    "description": "Call to action."
                                }
                            },
                            "required": [
                                "hooks",
                                "angle",
                                "cta"
                            ]
                        },
                        "channel": {
                            "type": "string",
                            "description": "Recommended outreach channel."
                        }
                    },
                    "required": [
                        "qualification",
                        "opportunity",
                        "offer",
                        "reason",
                        "angle"
                    ]
                }
            }
        }
    ]


    client = Groq(
            api_key=setting.GROQ_API_KEY
        )

    chat_completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content" : system_prompt
            },
            {
                "role" : "user",
                "content" : outreach_input

            }
        ],
        tools=tools
    )


    if chat_completion.choices[0].message.tool_calls[0]:
        logger.info("Tool Called!")
        tool = chat_completion.choices[0].message.tool_calls[0]
        arguments = json.loads(tool.function.arguments)
        tool_id = tool.id
        info_req = offer_tool_input(
        pain=arguments["opportunity"]["pain"],
        urgency=arguments["opportunity"]["urgency"],
        problem=arguments["offer"]["problem"],
        desirable_outcome=arguments["offer"]["desirable_outcome"],
        proof=arguments["offer"]["proof"],
        low_risk=arguments["offer"]["low_risk"],
        value=arguments["offer"]["value"]
        )


        offer_input = info_req.model_dump_json()
        review_strategy = offerrefine(offer_input)
        data = json.loads(outreach_input)
        data["refined_offer"] = review_strategy.refine_offer
        outreach_input = json.dumps(data)
        logger.info("strategy Reviewed")
        result = outreach_message(outreach_input)
        print(result)
        return result
    else:
        logger.info("TOOL CALLED NOT REQUIRED")
        result = outreach_message(outreach_input)
        print(result)
        logger.info("Successfully Generated Message")
        return result



    


    



def outreach_message(outreach_input):
    system_prompt = """
    ## ROLE ##
    Act as an Expert Copywriter Specialize in writing attention grabbing and persuasive cold outreach message for prospects.
    You are master of this field who understand human pyschology, persuasion, Sales technique.
    
    

    ## OUTPUT ##

    Using the Research Result, Strategy Result, and the channel selected by the user, write ONE personalized cold outreach message for that channel.

    The user will provide exactly one channel:
    - email
    - linkedin
    - instagram
    - facebook

    Generate content ONLY for the selected channel.
    Do not generate content for any other channel.

    Return only valid JSON using this structure:

    {
        "channel": "string",
        "outreach_msg": {
            "subject_line": "string",
            "message": "string",
            "cta": "string"
        }
    }

    FIELD DEFINITIONS:

    channel:
        - The exact channel selected by the user.

    subject_line:
        - Required only for email.
        - For LinkedIn, Instagram, or Facebook, return an empty string.
        - Make the subject relevant and specific enough to earn attention.
        - Do not use clickbait, exaggerated claims, or artificial pattern-interrupt language.

    message:
        - The complete outreach message.
        - For email, this is the email body.
        - For LinkedIn, Instagram, or Facebook, this is the complete DM.

    cta:
        - One simple, low-friction call to action.
        - The primary goal is to encourage a reply.
        - Do not ask for a call, booking, purchase, or other commitment unless explicitly supported by the Strategy Result.


    
    
                
    Tone and voice :
    Write like a sharp, experienced operator talking to one intelligent person. Be direct, conversational, specific, and confident. Never sound like a marketer trying to sound persuasive. Don't exaggerate. Don't use corporate jargon. Don't manufacture enthusiasm. Don't over-explain. Create relevance quickly, identify a real problem or opportunity, provide a useful insight, and make the next step extremely easy.
    Never try to sound like Alex Hormozi, Sabri Suby, or Alex Cattoni. Extract the principles that make their copy effective, then write in a natural voice appropriate to the prospect

    ## RULES ##
    
    COPYWRITING RULES:
    1. Write for one specific person.
    2. Lead with relevance, not introduction.
    3. Focus on their problem, not your service.
    4. Be specific, never generic.
    5. Use simple, conversational language.
    6. Create curiosity without hype or clickbait.
    7. Give value before asking for anything.
    8. Be confident without sounding arrogant.
    9. Make the CTA small and low-friction.
    10.Cut anything that doesn't improve clarity, relevance, persuasion, or curiosity.
    11. Only personalize using prospect-specific information explicitly present in the Research Result or Strategy Result. Never invent observations about the prospect, their performance, customers, team, goals, or recent activity.

    PERSUASIVE CLAIM CONSTRAINT

    - Do not turn a supported pain point into an unsupported consequence.
    - Do not turn a potential benefit into an expected outcome.
    - Do not add causal relationships between the prospect's problem and business performance unless explicitly supported.
    - Do not use phrases such as "you're losing", "you're missing", "this is costing you", "this will increase", "this will generate", or similar claims unless the underlying claim is explicitly supported.
    - Words such as "may", "might", "could", or "likely" do not make an unsupported claim acceptable.
    - Do not imply firsthand observation using phrases such as "I noticed", "I saw", "I found", or "looking at your..." unless that observation is explicitly supported by the Research Result.
    - Do not fabricate the sender's personal observations, experience, expertise, client history, previous results, or interactions. If a claim about the sender is not provided by the user or supported by the Strategy Result, do not include it.
    OTHER RULES:
    1. You must write the message based on research and strategy provided.
    2. Do not introduce new factual claims, problems, circumstances, numbers, or outcomes. You may naturally rephrase supported information without changing its meaning.
    3. You must write the message among angles mentioned on strategy.
    4. Do not use any info , pain, or claim the numbers in message which is not in research and strategy.
    5. If the information regarding research and strategy is too low to write the message you must use that without adding based on assumptions or general generic copy
    6. Do not create, expand, or modify the offer. Use only the problem, outcome, proof, value, and low-risk mechanism provided by the Strategy Agent.
    7. You must use proof and low_risk from strategy if needed. 
    8. You must target opportunity or pain points from strategy without adding any extra info.
    9. Do not convert a research/strategy description into a firsthand observation about the prospect unless the source explicitly states that the observation was made.
    10. Do not introduce causal relationships, customer behavior, performance claims, or expected outcomes when they are not explicitly supported by the Research Result, Strategy Result, or user-provided information.
    
    """

   
    client = Groq(
        api_key=setting.GROQ_API_KEY
    )

    chat_completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content" : system_prompt
            },
            {
                "role" : "user",
                "content" : outreach_input

            }
        ],
        response_format={
            "type":"json_object",
            "json_object": {
                "name": "Outreach_Message",
                "strict" : True,
                "schema": Outreach_Message.model_json_schema()
            }
        }
    )
    response = chat_completion.choices[0].message.content
    outreach_result = Outreach_Message(**json.loads(response))
    print(outreach_result)
    return outreach_result







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
    review(outreach_input)
    

