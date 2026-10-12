from config.settings import setting
from config.logger import logger
from groq import Groq
from research.research_analyzer import research_agent_workflow, clean_html, fetch_all, user_data, url_classification,fetch_homepage,normalize_deduplicate_links
from strategy.strategy_agent import strategy_agent_workflow
from models.outreach_schema import Outreach_Message,Email_Outreach
from models.research_tool_schema import offer_tool_input
from models.workflow_state import state
from tools.strategy_review import offerrefine
from google import genai
from google.genai import types
import asyncio
import json
import time
from pydantic import ValidationError
import random
from google.genai.errors import ServerError

def _log_event(level, stage, *, exc_info=False, **details):
    event = {
        "stage": stage,
        **details,
    }
    getattr(logger, level)(
        json.dumps(event, default=str),
        exc_info=exc_info,
    )

def log_llm_usage(stage, chat_completion, latency):
    usage = chat_completion.usage
    _log_event(
        "info",
        stage,
        model=chat_completion.model,
        duration_seconds=round(latency, 2),
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
    )

def outreach_input_validation(result):
    if not isinstance(result, dict):
        raise ValueError("Outreach input must be an object")

    for field in (
        "user_service",
        "qualification",
        "fit",
        "fit_reasons",
        "offer",
        "angle",
        "reasoning",
        "channel",
        "service",
        "proof",
    ):
        if field not in result:
            raise ValueError(f"Missing required field: {field}")

    for field in ("user_service", "qualification", "channel", "service", "proof"):
        if not isinstance(result[field], str):
            raise ValueError(f"{field} must be a string")

    if not result["user_service"].strip():
        raise ValueError("User Service Is Empty")

    if result["qualification"] not in {"strong", "medium", "low"}:
        raise ValueError("qualification must be strong, medium, or low")

    if result["fit"] not in {"strong", "moderate", "weak", "insufficient_evidence"}:
        raise ValueError("fit must be one of strong, moderate, weak, insufficient_evidence")

    if not isinstance(result["fit_reasons"], list):
        raise ValueError("fit_reasons must be a list")

    if not isinstance(result["offer"], dict):
        raise ValueError("offer must be an object")
    for field in ("problem", "desirable_outcome", "proof", "low_risk", "value"):
        if field not in result["offer"] or not isinstance(result["offer"][field], str):
            raise ValueError(f"offer.{field} must be a string")

    if not isinstance(result["angle"], dict):
        raise ValueError("angle must be an object")
    for field in ("hooks", "angle", "cta"):
        if field not in result["angle"]:
            raise ValueError(f"Missing required field: angle.{field}")
    if not isinstance(result["angle"]["hooks"], list):
        raise ValueError("angle.hooks must be a list")
    for hook in result["angle"]["hooks"]:
        if not isinstance(hook, str) or not hook.strip():
            raise ValueError("angle.hooks must contain non-empty strings")
    if not isinstance(result["angle"]["angle"], str):
        raise ValueError("angle.angle must be a string")
    if not isinstance(result["angle"]["cta"], str):
        raise ValueError("angle.cta must be a string")

    if not isinstance(result["reasoning"], dict):
        raise ValueError("reasoning must be an object")
    if not isinstance(result["reasoning"].get("reason"), list):
        raise ValueError("reasoning.reason must be a list")

    if result["channel"] not in {"email", "linkedin", "instagram", "facebook"}:
        raise ValueError("channel must be one of email, linkedin, instagram, facebook")


def validate_outreach_business_rules(result):
    errors = []

    if result["qualification"] == "strong" and result["fit"] == "weak":
        errors.append("Strong qualification conflicts with weak fit")

    if result["fit"] == "insufficient_evidence" and result["qualification"] != "low":
        errors.append("Insufficient evidence requires low qualification")

    if not result.get("fit_reasons"):
        errors.append("fit_reasons is empty")

    if not result.get("angle", {}).get("hooks"):
        errors.append("angle.hooks is empty")

    if errors:
        raise ValueError(errors)


def _safe_tool_calls(chat_completion):
    choices = getattr(chat_completion, "choices", None)
    if not choices:
        logger.warning("Tool-call response has no choices")
        return []

    message = getattr(choices[0], "message", None)
    tool_calls = getattr(message, "tool_calls", None) if message else None

    if tool_calls is None:
        return []
    if not isinstance(tool_calls, (list, tuple)):
        logger.warning("Tool calls have an invalid response type")
        return []

    return list(tool_calls)


def _safe_tool_arguments(tool):
    function = getattr(tool, "function", None)
    if function is None:
        raise ValueError("Tool call is missing its function")

    tool_name = getattr(function, "name", None)
    if tool_name != "offerrefine":
        raise ValueError(f"Unexpected tool: {tool_name}")

    raw_arguments = getattr(function, "arguments", None)
    try:
        arguments = raw_arguments if isinstance(raw_arguments, dict) else json.loads(raw_arguments)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("Tool arguments are missing or invalid JSON") from exc

    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be a JSON object")

    required_top = [
        "qualification",
        "fit",
        "fit_reasons",
        "offer",
        "angle",
        "reasoning",
        "channel",
        "service",
        "proof",
    ]

    for field in required_top:
        if field not in arguments:
            raise ValueError(f"Missing required field: {field}")

    if arguments["qualification"] not in {"strong", "medium", "low"}:
        raise ValueError("qualification must be one of strong, medium, low")

    if arguments["fit"] not in {"strong", "moderate", "weak", "insufficient_evidence"}:
        raise ValueError("fit must be one of strong, moderate, weak, insufficient_evidence")

    if not isinstance(arguments["fit_reasons"], list):
        raise ValueError("fit_reasons must be a list")

    offer = arguments["offer"]
    if not isinstance(offer, dict):
        raise ValueError("offer must be an object")
    for field in ("problem", "desirable_outcome", "proof", "low_risk", "value"):
        if not isinstance(offer.get(field), str):
            raise ValueError(f"offer.{field} must be a string")

    angle = arguments["angle"]
    if not isinstance(angle, dict):
        raise ValueError("angle must be an object")
    for field in ("hooks", "angle", "cta"):
        if field not in angle:
            raise ValueError(f"angle.{field} missing")
    if not isinstance(angle["hooks"], list):
        raise ValueError("angle.hooks must be a list")
    for hook in angle["hooks"]:
        if not isinstance(hook, str) or not hook.strip():
            raise ValueError("angle.hooks contains an empty value")
    if not isinstance(angle["angle"], str):
        raise ValueError("angle.angle must be a string")
    if not isinstance(angle["cta"], str):
        raise ValueError("angle.cta must be a string")

    reasoning = arguments["reasoning"]
    if not isinstance(reasoning, dict):
        raise ValueError("reasoning must be an object")
    if not isinstance(reasoning.get("reason"), list):
        raise ValueError("reasoning.reason must be a list")

    return arguments


def offer_tool_calling(chat_completion):
    tool_calls = _safe_tool_calls(chat_completion)
    if not tool_calls:
        raise ValueError("No tool calls were returned")

    logger.info("Tool Called!")
    arguments = _safe_tool_arguments(tool_calls[0])

    fit_reasons = arguments.get("fit_reasons", []) or []
    pain = [str(reason).strip() for reason in fit_reasons if str(reason).strip()]

    info_req = offer_tool_input(
        pain=pain,
        problem=str(arguments["offer"]["problem"]),
        desirable_outcome=str(arguments["offer"]["desirable_outcome"]),
        proof=str(arguments["offer"]["proof"]),
        low_risk=str(arguments["offer"]["low_risk"]),
        value=str(arguments["offer"]["value"])
    )

    offer_input = info_req.model_dump_json()
    refined_offer = offerrefine(offer_input)
    return refined_offer


def outreach_toolcall_check(outreach_input):
    system_prompt = """
    ## ROLE ##
    Act as an expert cold-outreach copywriter specializing in attention-grabbing and persuasive outreach messages.

    You understand sales psychology, persuasion, and effective offer positioning.

    Before writing the outreach message, evaluate the offer.
    If it is materially weak, call the tool named `offerrefine`.
    Otherwise, do not call a tool.

    Do not return JSON. Do not call any tool other than `offerrefine`.

    ## RULES ##
    - Use the current Strategy_result schema exactly.
    - Do not invent data.
    - Only call the tool when the offer is materially weak.
    - If the offer is already strong and usable, do not call the tool.
    - The tool input must only use fields from the current Strategy_result schema:
      qualification, fit, fit_reasons, offer, angle, reasoning, channel, service, proof
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
                            "enum": ["strong", "medium", "low"]
                        },
                        "fit": {
                            "type": "string",
                            "enum": ["strong", "moderate", "weak", "insufficient_evidence"]
                        },
                        "fit_reasons": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "offer": {
                            "type": "object",
                            "properties": {
                                "problem": {"type": "string"},
                                "desirable_outcome": {"type": "string"},
                                "proof": {"type": "string"},
                                "low_risk": {"type": "string"},
                                "value": {"type": "string"}
                            },
                            "required": [
                                "problem",
                                "desirable_outcome",
                                "proof",
                                "low_risk",
                                "value"
                            ]
                        },
                        "angle": {
                            "type": "object",
                            "properties": {
                                "hooks": {"type": "array", "items": {"type": "string"}},
                                "angle": {"type": "string"},
                                "cta": {"type": "string"}
                            },
                            "required": ["hooks", "angle", "cta"]
                        },
                        "reasoning": {
                            "type": "object",
                            "properties": {
                                "reason": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["reason"]
                        },
                        "channel": {"type": "string"},
                        "service": {"type": "string"},
                        "proof": {"type": "string"}
                    },
                    "required": [
                        "qualification",
                        "fit",
                        "fit_reasons",
                        "offer",
                        "angle",
                        "reasoning",
                        "channel",
                        "service",
                        "proof"
                    ]
                }
            }
        }
    ]

    client = Groq(api_key=setting.GROQ_API_KEY)
    start = time.perf_counter()
    chat_completion = client.chat.completions.create(
        model=setting.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": outreach_input}
        ],
        tools=tools,
        tool_choice="auto",
    )

    state.total_token_used += chat_completion.usage.total_tokens
    state.input_tokens += chat_completion.usage.prompt_tokens
    state.output_tokens += chat_completion.usage.completion_tokens

    log_llm_usage(
        "outreach_toolcall_check",
        chat_completion,
        time.perf_counter() - start,
    )
    return chat_completion


def outreach_message(outreach_input):
    input_data = json.loads(outreach_input) if isinstance(outreach_input, str) else outreach_input
    channel = input_data.get("channel", "").strip().lower()
    response_model = Email_Outreach if channel == "email" else Outreach_Message

    system_prompt = """
    ## ROLE

    Act as an expert cold outreach copywriter specializing in concise, personalized, conversational outreach.

    Your job is to turn the provided **Research Result + Strategy Result** into a compelling message without creating new information.

    ## CORE PRINCIPLE

    **Research determines what is known.
    Strategy determines what should be communicated.
    Copywriting determines how it is communicated.**

    Your creativity applies only to **expression**, never to **information**.

    You may improve:

    * wording
    * structure
    * flow
    * clarity
    * conversational tone
    * curiosity
    * brevity

    You must not add or strengthen:

    * problems or pain points
    * causes or consequences
    * prospect intent
    * urgency or timing
    * customer behavior
    * business impact
    * benefits or outcomes
    * assumptions about what the prospect wants
    * claims about what the prospect is experiencing
    * offer components or deliverables
    * proof or credentials

    If something is not supported by the provided context, leave it out.

    ---

    ## INPUTS

    You will receive:

    1. **Strategy Result** — the approved service, opportunity, offer, angle, hook, proof, and CTA.
    2. **Channel** — one of:

    * email
    * linkedin
    * instagram
    * facebook

    The **Research Result is the source of truth for prospect facts.**

    The **Strategy Result defines the approved messaging direction.**

    Do not expand either one with your own assumptions.

    ---

    ## TASK

    Write **ONE personalized cold outreach message** using the selected channel.

    The message should:

    * use the strongest supported prospect-specific context
    * follow the selected strategy and angle
    * clearly connect the service to the approved opportunity
    * use only provided proof and offer details
    * keep the CTA low-friction and consistent with the Strategy Result
    * sound natural rather than promotional

    If the provided context is insufficient to write a credible personalized message, return the required empty JSON instead of filling the gaps yourself.

    ---

    ## PERSUASION BOUNDARY

    Persuasion must come from **how the approved information is framed**, not from adding new information.

    Do not reason beyond the context to make the message stronger.

    For example:

    **Supported:**

    > "They recently launched online ordering."

    Allowed:

    > "Saw you recently launched online ordering."

    Not allowed:

    > "Saw you recently launched online ordering. You may already be losing customers because of the experience."

    The second sentence introduces an unsupported consequence and customer behavior.

    A claim being plausible, common, commercially logical, or persuasive does **not** make it supported.

    ---

    ## PERSONALIZATION

    Personalization must be based only on explicit information in the provided context.

    Do not manufacture:

    * observations about the website
    * customer behavior
    * business challenges
    * goals
    * frustrations
    * motivations
    * internal priorities

    If there is no valid personalization signal, do not invent one.

    ---

    ## STYLE

    * Simple and conversational.
    * Direct and concise.
    * Prospect-focused.
    * Avoid generic AI/marketing language.
    * Avoid unnecessary jargon.
    * Avoid exaggerated or absolute language.
    * Do not use fake compliments or filler.
    * Do not sound like a mass-produced template.
    * Do not imitate a specific person's writing style.

    ---

    ## CHANNEL RULES

    ### email

    * Include a relevant, non-clickbait subject line.
    * Keep the body concise.
    * CTA should encourage a reply.

    ### linkedIn

    * No subject line.
    * Keep it conversational and concise.
    * Aim for roughly 50–90 words when the context supports it.

    ### instagram

    * No subject line.
    * Write naturally for a DM.
    * Keep it short and conversational.

    ### facebook

    * No subject line.
    * Write naturally for a DM.
    * Keep it short and conversational.

    ---

    ## CTA

    Use the CTA provided by the Strategy Result when available.

    Do not introduce a call, meeting, booking, purchase, audit, demo, trial, or other commitment unless explicitly supported by the Strategy Result.

    ---

    ## FINAL CHECK

    Before producing the message, verify:

    1. Every prospect-specific claim is supported by the Research Result.
    2. Every strategic claim is supported by the Strategy Result or Research Result.
    3. No inference has been presented as a fact.
    4. No new pain, consequence, outcome, urgency, intent, or business impact has been introduced.
    5. The offer and proof have not been expanded.
    6. The message is persuasive through wording, not invented information.
    7. When research contains conflicting information, do not resolve, reconcile, or reinterpret the conflict. Only use a claim if it is independently supported by the available information.

    If any sentence fails these checks, rewrite or remove it.

    ---

    ## OUTPUT

    Return only valid JSON.

    If channel is facebook | instagram | linkedin return in this format:

    ```json
    {
    "channel": "string",
    "outreach_msg": {
       "message" : "string",
    }
    }
    ```

    if channel is email return in this format:
    
    ```json
    {
    "channel": "string",
    "outreach_msg": {
        "subject_line": "",
        "message": "",
        "cta": ""
    }
    }
    ```

 
    """
    
    start = time.perf_counter()
    client = genai.Client(
        api_key=setting.GEMINI_API_KEY,
        http_options=types.HttpOptions(timeout=60_000),  # milliseconds
    )

    response = None
    for attempt in range(3):
        if attempt == 2:
            model = setting.GEMINI_MODEL_2
        else:
            model = setting.GEMINI_MODEL
        try:
            logger.info("Sending outreach request to Gemini")
            response = client.models.generate_content(
                model=model,
                contents=outreach_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=response_model,
                ),
            )
            logger.info("Gemini outreach response received")
            break
        except ServerError:
            if attempt == 2:
                logger.exception("Gemini remained unavailable after retries")
                raise
            time.sleep((2 ** attempt) + random.uniform(0, 1))

    usage = getattr(response, "usage_metadata", None)
    if usage:
        input_tokens = getattr(usage, "prompt_token_count", 0) or 0
        output_tokens = getattr(usage, "candidates_token_count", 0) or 0
        total_tokens = getattr(usage, "total_token_count", None)
        state.input_tokens += input_tokens
        state.output_tokens += output_tokens
        state.total_token_used += total_tokens or input_tokens + output_tokens

    response_text = response.text
    if not response_text or not response_text.strip():
        raise ValueError("Model returned an empty outreach response")

    try:
        outreach_result = response_model.model_validate_json(response_text)
    except ValidationError as exc:
        logger.exception("Model outreach response failed schema validation")
        raise ValueError(
            f"Model outreach response does not match the {channel!r} schema"
        ) from exc

    _log_event(
        "info",
        "outreach_message.completed",
        model=model,
        duration_seconds=round(time.perf_counter() - start, 2),
        input_tokens=input_tokens if usage else 0,
        output_tokens=output_tokens if usage else 0,
        total_tokens=total_tokens if usage and total_tokens is not None else 0,
    )
    return outreach_result



def outreach_agent_workflow(result):
    _log_event("info", "outreach_workflow.started")
    try:
        logger.info("Starting Outreach Input and Business Rules Validation")
        outreach_input_validation(result)
        validate_outreach_business_rules(result)

        angle = result.get("angle") or {}
        hooks = angle.get("hooks") or []
        fit_reasons = result.get("fit_reasons") or []

        if not fit_reasons or not hooks:
            _log_event("info", "outreach_workflow.no_recommendation")
            return Outreach_Message(
                channel=result["channel"],
                outreach_msg={
                    "subject_line": "",
                    "message": "",
                    "cta": "",
                },
            )

        outreach_input = json.dumps(result)
    except Exception as exc:
        _log_event(
            "error",
            "outreach_input.validation_failed",
            error_type=type(exc).__name__,
            exc_info=True,
        )
        raise

    try:
        chat_completion = outreach_toolcall_check(outreach_input)
    except Exception as exc:
        _log_event(
            "error",
            "outreach_tool_check.failed",
            error_type=type(exc).__name__,
            exc_info=True,
        )
        raise

    tool_calls = _safe_tool_calls(chat_completion)
    if tool_calls:
        try:
            refined_offer = offer_tool_calling(chat_completion)
            data = json.loads(outreach_input)
            data["refined_offer"] = refined_offer.refine_offer
            outreach_input = json.dumps(data)
            _log_event("info", "offer_refinement.completed")
        except Exception as exc:
            _log_event(
                "error",
                "offer_refinement.failed",
                error_type=type(exc).__name__,
                exc_info=True,
            )
            # Continue with the original outreach_input if refinement fails.
    else:
        _log_event("info", "offer_refinement.not_needed")

    try:
        outreach_result = outreach_message(outreach_input)
        _log_event("info", "outreach_workflow.completed")
        print("Outreach Result:", outreach_result)
        return outreach_result
    except Exception as exc:
        _log_event(
            "error",
            "outreach_message.failed",
            error_type=type(exc).__name__,
            exc_info=True,
        )
        raise





if __name__ == "__main__":
    strategy_input = {
        "user_service": "LEAD GENERATION",
        "qualification": "strong",
        "fit": "strong",
        "fit_reasons": [
            "They have a clear service business and likely need more booked leads.",
            "The offer is low-risk and directly tied to their website conversion."
        ],
        "offer": {
            "problem": "They may be missing a clear conversion path on their website.",
            "desirable_outcome": "A website that captures more qualified leads and inquiries.",
            "proof": "7+ years of experience",
            "low_risk": "No Money Until One Patient",
            "value": "More consistent lead flow from the website."
        },
        "angle": {
            "hooks": [
                "A clearer conversion path",
                "More qualified inbound leads"
            ],
            "angle": "Focus on making the website easier for qualified buyers to contact them.",
            "cta": "Would it be worth a quick review of your site conversion path?"
        },
        "reasoning": {
            "reason": [
                "The company is service-based and likely depends on website conversion.",
                "The offer is low-risk and relevant to their business."
            ]
        },
        "channel": "instagram",
        "service": "LEAD GENERATION",
        "proof": "7+ years of experience"
    }

    
    # user_service, low_risk, proof = user_data()
    # url = "https://www.vistadentalimplants.com/"

    # page_content, links  = asyncio.run(fetch_homepage(url))
    # urls = normalize_deduplicate_links(links,url)
    # selected_pages_url = url_classification(urls)
    # selected_pages_url.append({"url":url, "page_type":"Home"})
    # page_content = asyncio.run(fetch_all(selected_pages_url))
    # content = clean_html(page_content)
    # content = content.model_dump()
    # result = research_agent_workflow(content,user_service)
    # result.user_service = user_service
    # result.user_proof = proof
    # result.user_low_risk = low_risk
    # strategy_input = result.model_dump()
    # strategy_result = strategy_agent_workflow(strategy_input)
    # result_strategy = strategy_result.model_dump()
    # result_strategy["channel"] = "instagram"
    # result_strategy["user_service"] = user_service
    outreach_agent_workflow(strategy_input)


