from models.research_tool_schema import SearchWeb
from groq import Groq
from config.settings import setting
import json
from config.logger import logger
from models.workflow_state import state



def search_web(industry):
    system_prompt = """
    ## ROLE ##
    Act as an expert in Market Research. You specialize in researching prospect market very deeply based on evidence.

    ## Output ##
    Return the result as valid JSON matching the structure below.
    { 
       "pain_points" : [{"Pain_Point":value, "Evidence":Link}],
       "avilable_solutions" : list[str],
       "satisfied" : bool,
       "resources" : list[str]
 
       
    }

    ## Field Definations ##
    - pain_points : You must provide the list of pain points the industry mention is facing based on evidence.
        For Each Pain Point You must Give the citation link for that pain point
    - avilable_solutions : You must list down what avilable_solutions industry using to solve their pain points
    - satified : This field tells the solutions they're using are they satisfied with it, if industry tells that they happy with current solutions then return True else False
    - resources : list down the public forums name you used to do the research
    ## RULES ##
    - You must do the research based on the industry mentioned.
    - You must use only public forums or credible articles to do the research.
    - Do not include irrelevant information.
    - Do not invent, assume, or hallucinate information.
    - Return only the structured result. Do not add explanations outside the structure.


    """
    try:
        client = Groq(
            api_key= setting.GROQ_API_KEY
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
                    "content" : industry
                }
            ],
            response_format={
                "type" : "json_object",
                "json_object" : {
                    "name" : "SearchWeb",
                    "strict" : True,
                    "schema" : SearchWeb.model_json_schema()
                }
            }
        )
        state.total_token_used += chat_completion.usage.total_tokens
        state.input_tokens += chat_completion.usage.prompt_tokens
        state.output_tokens += chat_completion.usage.completion_tokens
        response = chat_completion.choices[0].message.content
        result = SearchWeb(**json.loads(response))
        print(result)
    
        return result

    except Exception as e:
        logger.error("Failed to Research Industry!", e)



if __name__ == "__main__":
    industry = "web designing"

    search_web(industry)

