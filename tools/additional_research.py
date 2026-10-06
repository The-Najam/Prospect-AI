from groq import Groq
from config.settings import setting
from models.research_tool_schema import additional_research
from models.workflow_state import state
import json
from config.logger import logger


def missing_info_research(company_data):
    print("IN TOOL CALLL")
    company_data = json.dumps(company_data)
    prompt = """
    Act as an expert market researcher specializing in prospect and market research.

    ## OUTPUT ##
    Return the output only in JSON format.
    {
        additional_info : list[str]
    
    }

    ## RULES ##
    Use the provided company data, ICP type, and missing information to guide the research.
    Research publicly available sources, including relevant forums such as Reddit and Quora.
    Focus only on the missing information in the context.
    Do not invent, assume, or hallucinate information.
    Include only information supported by the research.
    Keep the findings concise and relevant to prospect research and qualification.
    Return only the structured result. Do not add explanations outside the structure.
    
    """

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
                "content": company_data
            }
        ],
        response_format={
            "type" : "json_object",
            "json_object" : {
                "name" : "additional_research",
                "strict" : True,
                "schema" : additional_research.model_json_schema()
            }
        }
    )
    state.total_token_used += chat_completions.usage.total_tokens
    state.input_tokens += chat_completions.usage.prompt_tokens
    state.output_tokens += chat_completions.usage.completion_tokens
    response = chat_completions.choices[0].message.content

    print(response)
    response = additional_research(**json.loads(response))
    print(type(response))
    logger.info("MISSING INFO FINDED")
    

    return response





if __name__ == "__main__":
   
    company_data = """{
    "CompanyData": {
        "name": "Elevate",
        "about": "A web design agency providing website design and redesign services for small businesses.",
        "location": "United States",
        "industry": "Web Design Services",
        "Company_size": "10-25 employees"
    },
    "services": {
        "services": [
        {
            "name": "Website Design",
            "description": "Custom website design for small and medium-sized businesses.",
            "Pricing": "Starting at $2,500"
        },
        {
            "name": "Website Redesign",
            "description": "Redesigning outdated business websites to improve usability and conversion.",
            "Pricing": "Starting at $3,500"
        }
        ]
    },
    "icp": {
        "Type": "Small and medium-sized business owners",
        "location": "United States",
        "Needs": [],
        "Buying_behavior": "",
        "Objections": ""
    },
    "opportunties": {
        "Pain_points": []
    }
    }"""
    missing_info_research(company_data)
