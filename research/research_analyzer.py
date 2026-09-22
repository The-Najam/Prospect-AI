from research.data_cleaner import clean_html
from research.data_extraction import main
from models.research_schemas import Research_result
from models.research_tool_schema import social_media_extractor
from tools.media_info_extraction import extraction
from tools.web_search import search_web
import asyncio
from config.settings import setting
from config.logger import logger
from groq import Groq
import json


def analyzer(content):
    pages = "\n\n".join(
    page["page_content"]
    for page in content
)
    

    system_prompt = """Act as an Expert Company Research Analyist specialize in extracting structured prospect research by analyzing the website content
    Analyze the provided website content and extract only information relevant to prospect research and qualification from the Cleaned text extracted from multiple pages of a company's website.


    ## OUTPUT ##
    Return the result as valid JSON matching the structure below.
     
    {
    "CompanyData": {
        "name": "string",
        "about": "string",
        "location": "string",
        "industry": "string",
        "Company_size": "string"
    },

    "services": {
        "services": [
        {
            "name": "string",
            "description": "string",
            "Pricing": "string"
        }
        ]
    },

    "icp": {
        "Type": "string",
        "location": "string",
        "Needs": ["string"],
        "Buying_behavior": "string",
        "Objections": "string"
    },

    "opportunties": {
        "Pain_points": ["string"]
    }
    }


    FIELD DEFINITIONS:

    CompanyData:
    - name: The company's official name.
    - about: A concise description of what the company does.
    - location: Company's headquarters or primary location.
    - industry: The primary industry the company operates in.
    - Company_size: Employee count, company size category, or other available indication of company size.

    services:
    - services: List ALL clearly identifiable products or services offered by the company.
    - name: Name of the service/product.
    - description: Short description of what the service/product provides.
    - Pricing: Pricing information if explicitly available. Do not guess or estimate.

    icp:
    - Type: The category or type of customers/businesses the company targets, such as B2B, B2C, startups, SMBs, enterprises, e-commerce businesses, or specific industries.
    - location: Geographic markets or locations the company targets.
    - Needs: Customer needs that the company's services/products address.
    - Buying_behavior: Any evidence about how customers purchase or evaluate the company's services.
    - Objections: Customer concerns or barriers to purchasing that are explicitly mentioned or directly supported by the website content.

    opportunties:
    - Pain_points: Customer problems or pain points that the company's services/products appear to solve.


    ## RULES ##
    1. Extract information only from the provided website content.
    2. Do not invent, assume, or hallucinate information.
    3. If information is not available, use an empty string or empty list.
    4. Keep information concise and relevant to prospect research and qualification.
    5. Do not include irrelevant company information.
    6. For pricing, only include pricing explicitly stated on the website.
    7. If multiple services exist, return each service as a separate object in the services list.
    8. Distinguish between facts stated on the website and assumptions. Do not include unsupported assumptions.
    9. Return only the structured result. Do not add explanations outside the structure.

    ## INFERENCE RULES ##
    1. Explicit information → always allowed : if website content directly reflect the info research needs than you have to include it.
    2. Evidence-based inference → allowed, but clearly treated as an inference
    But it must not present that as a confirmed company pain point.
    | Field           | Rule                                               |
    | --------------- | -------------------------------------------------- |
    | Company Data    | **Explicit only**                                  |
    | Services        | **Explicit only**                                  |
    | ICP             | **Explicit + reasonable evidence-based inference** |
    | Needs           | **Explicit + evidence-based inference**            |
    | Buying Behavior | **Explicit + cautious inference**                  |
    | Objections      | **Explicit + cautious inference**                  |
    | Pain Points     | **Explicit + evidence-based inference**            |

    Unsupported assumptions are prohibited. Evidence-based inferences are allowed only when they are directly supported by information in the provided website content, and inferred information must be phrased as a potential/likely observation rather than a confirmed fact.
     
    

    - Social Profile Research: When social profile URLs are available and the information from their bios could materially improve the research, use the social bio extraction tool. The tool is optional; do not call it when the available information is sufficient or social bios are irrelevant. Use the returned bio information as additional context when producing the final research result.
    - if you need the Social Profile Research research just return
    
    
    
    """
    tools = [
        {
            "type" : "function",
            "function" : {
                "name" : "Social_Bio_Info",
                "description": "Extract bios from supplied social profile URLs.",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "social_urls" : {
                            "type" : "array",
                            "items" : {
                                "type" : "string"
                            }
                        }
                    },
                    "required": ["social_urls"]
                }
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "Web_Search",
                "description" : "Do Web Search to extract more context about industry and market",
                "parameters":{
                    "type" : "object",
                    "properties" :{
                        "industry" : {
                            "type" : "string"
                        }
                        }
                    },
                    "required" : [
                        "industry"
                    ]
                }

            }
    ]


    try:
        client = Groq(
        api_key=setting.GROQ_API_KEY
        )

        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": pages
                }
            ],
            tools=tools
        )
       
        if chat_completion.choices[0].message.tool_calls: 
            try:
                tools_call = chat_completion.choices[0].message.tool_calls
                for tool in tools_call:
                    if tool.function.name == "Social_Bio_Info":
                        logger.info("Tool Call Detected!")
                        arguments = json.loads(tool.function.arguments)
                        social_urls = arguments["social_urls"]
                        tool_id = tool.id
                        additional_info = asyncio.run(extraction(social_urls))
                        tool_result = {
                                "role" : "tool",
                                "tool_call_id" : tool_id,
                                "content" : additional_context
                            }
                        content.append(tool_result)
                    elif tool.function.name == "Web_Search":
                        logger.info("Web Search tool Called")
                        arguments = json.loads(tool.function.arguments)
                        industry = arguments["industry"]
                        tool_id = tool.id
                        additional_context = search_web(industry)
                        tool_result = {
                            "role" : "tool",
                            "tool_call_id" : tool_id,
                            "content" : additional_context
                        }

                        content.append(tool_result)
        
                final_response = second_call(content)
                return final_response
            except Exception as e:
                logger.error("Failed To Call Tool", e)


        else:
            logger.info("Tool Call Not Detected!")
            result = second_call(content)
            return result
    except Exception as e:
        logger.error("Research Can't be done", e)
    



def second_call(content):
    pages = "\n\n".join(
    page["page_content"]
    for page in content
)
    
    system_prompt = """Act as an Expert Company Research Analyist specialize in extracting structured prospect research by analyzing the website content
    Analyze the provided website content and extract only information relevant to prospect research and qualification from the Cleaned text extracted from multiple pages of a company's website.


    ## OUTPUT ##
    Return the result as valid JSON matching the structure below.
     
    {
    "CompanyData": {
        "name": "string",
        "about": "string",
        "location": "string",
        "industry": "string",
        "Company_size": "string"
    },

    "services": {
        "services": [
        {
            "name": "string",
            "description": "string",
            "Pricing": "string"
        }
        ]
    },

    "icp": {
        "Type": "string",
        "location": "string",
        "Needs": ["string"],
        "Buying_behavior": "string",
        "Objections": "string"
    },

    "opportunties": {
        "Pain_points": ["string"]
    }
    }


    FIELD DEFINITIONS:

    CompanyData:
    - name: The company's official name.
    - about: A concise description of what the company does.
    - location: Company's headquarters or primary location.
    - industry: The primary industry the company operates in.
    - Company_size: Employee count, company size category, or other available indication of company size.

    services:
    - services: List ALL clearly identifiable products or services offered by the company.
    - name: Name of the service/product.
    - description: Short description of what the service/product provides.
    - Pricing: Pricing information if explicitly available. Do not guess or estimate.

    icp:
    - Type: The category or type of customers/businesses the company targets, such as B2B, B2C, startups, SMBs, enterprises, e-commerce businesses, or specific industries.
    - location: Geographic markets or locations the company targets.
    - Needs: Customer needs that the company's services/products address.
    - Buying_behavior: Any evidence about how customers purchase or evaluate the company's services.
    - Objections: Customer concerns or barriers to purchasing that are explicitly mentioned or directly supported by the website content.

    opportunties:
    - Pain_points: Customer problems or pain points that the company's services/products appear to solve.


    ## RULES ##
    1. Extract information only from the provided website content.
    2. Do not invent, assume, or hallucinate information.
    3. If information is not available, use an empty string or empty list.
    4. Keep information concise and relevant to prospect research and qualification.
    5. Do not include irrelevant company information.
    6. For pricing, only include pricing explicitly stated on the website.
    7. If multiple services exist, return each service as a separate object in the services list.
    8. Distinguish between facts stated on the website and assumptions. Do not include unsupported assumptions.
    9. Return only the structured result. Do not add explanations outside the structure.

    ## INFERENCE RULES ##
    1. Explicit information → always allowed : if website content directly reflect the info research needs than you have to include it.
    2. Evidence-based inference → allowed, but clearly treated as an inference
    But it must not present that as a confirmed company pain point.
    | Field           | Rule                                               |
    | --------------- | -------------------------------------------------- |
    | Company Data    | **Explicit only**                                  |
    | Services        | **Explicit only**                                  |
    | ICP             | **Explicit + reasonable evidence-based inference** |
    | Needs           | **Explicit + evidence-based inference**            |
    | Buying Behavior | **Explicit + cautious inference**                  |
    | Objections      | **Explicit + cautious inference**                  |
    | Pain Points     | **Explicit + evidence-based inference**            |

    Unsupported assumptions are prohibited. Evidence-based inferences are allowed only when they are directly supported by information in the provided website content, and inferred information must be phrased as a potential/likely observation rather than a confirmed fact.
     s
    """

    try:
        client = Groq(
            api_key=setting.GROQ_API_KEY
        )
    
        chat_completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": pages
                    }
                ],
                response_format={
                    "type": "json_object",
                    "json_object": {
                        "name" : "Research_result",
                        "strict":True,
                        "schema": Research_result.model_json_schema()
                    }
                }
            )
        response = chat_completion.choices[0].message.content
        research_result = Research_result(**json.loads(response))
        logger.info("Research Completed Successfully")
        return research_result
    except Exception as e:
        logger.error("Research Can't be done", e)
        
    




        








if __name__ == "__main__":

    page_content = asyncio.run(main())
    content = clean_html(page_content)
    analyzer(content)
