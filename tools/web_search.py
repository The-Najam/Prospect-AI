
# importing Libraries
from models.research_tool_schema import WebSearchResult
from groq import Groq
from config.settings import setting
import json
from config.logger import logger
from models.workflow_state import WorkflowState
from langsmith import traceable,get_current_run_tree

# tracing Web Search tool call
@traceable(
    name="web_search_tool_call",
    run_type="tool",
    metadata={
        "ls_provider": "groq",
        "ls_model_name": setting.model,
    },
)

# Web Search tool 
def search_web(industry, user_service):
    system_prompt = """
    ## ROLE ##
    Act as an expert in Market Research. You specialize in researching prospect market very deeply based on evidence.

    ## Output ##
    Return the result as valid JSON matching the structure below.
    {
    "pain_points": [
        {"Pain_Point": "string", "Evidence": "https://example.com"}
    ],
    "available_solutions": ["string"],
    "satisfied": true,
    "resources": ["https://example.com"]
    }

    ## Field Definations ##
    - pain_points : You must provide the list of pain points the industry mention is facing based on evidence also which match the user service.
        For Each Pain Point You must Give the citation link for that pain point
    - available_solutions : You must list down what available_solutions user service can solve the industry's pain points
    - satisfied : This field tells the solutions they're using are they satisfied with it, if industry tells that they happy with current solutions then return True else False
    - resources : list down the public forums name you used to do the research
    ## RULES ##
    - You must do the research based on the industry and user service mentioned.
    - You must use only public forums or credible articles to do the research.
    - Do not include irrelevant information.
    - Do not invent, assume, or hallucinate information.
    - Return only the structured result. Do not add explanations outside the structure.


    """
    try:
        client = Groq(api_key=setting.GROQ_API_KEY_V2)
        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role" : "system",
                    "content" : system_prompt
                },
                {
                    "role" : "user",
                    "content" : f"Industry: {industry}\nUser Service: {user_service}"
                }
            ],
            response_format={
                "type" : "json_object",
                "json_object" : {
                    "name" : "WebSearchResult",
                    "strict" : True,
                    "schema" : WebSearchResult.model_json_schema()
                }
            }
        )
      
        response = chat_completion.choices[0].message.content
        result = WebSearchResult(**json.loads(response))
        usage = getattr(chat_completion, "usage", None)
        groq_tokens = getattr(usage, "total_tokens", 0) or 0

        run = get_current_run_tree()
        if run and usage:
            run.set(
                usage_metadata={
                    "input_tokens": usage.prompt_tokens,
                    "output_tokens": usage.completion_tokens,
                    "total_tokens": groq_tokens,
                }
            )
        return result, groq_tokens

    except Exception as e:
        logger.error("Failed to Research Industry!", exc_info=True)





if __name__ == "__main__":
    industry = "web designing"
    user_service = "web development"

    search_web(industry, user_service)

