# importing Libraries
from bs4 import BeautifulSoup
from models.web_extraction_schema import WebExtraction
from config.logger import logger
from models.workflow_state import WorkflowState


# cleaning Html from Extracted Raw Content
def clean_html(state:WorkflowState):
    content = []
    cleaned_content_attempts = state.get("cleaned_content_attempts", 0) + 1

    for page in state['page_content']:
        html = page.get("content")
        if not isinstance(html, (str, bytes)) or not html.strip():
            logger.warning("Skipping page with missing or empty HTML: %s", page.get("url"))
            continue
        url = page["url"]
        page_type = page["page_type"]
        soup = BeautifulSoup(html, "lxml")

        for tag in soup(["header", "nav", "footer", "script", "style"]):
            tag.decompose()
            
        text = soup.get_text(" ", strip=True)
        if text:
            content.append({"url": url, "page_type": page_type, "content": text})
    
    
    logger.info(f"CLEANING CONTENT ATTEMPT : {cleaned_content_attempts}")

    if not content:    
        logger.info(" No usable HTML content was fetched. Retrying Again!")
        return {
            "cleaned_content": content,
            "cleaned_content_attempts": cleaned_content_attempts,
        }
        
    else:
        clean_web_result = WebExtraction(pages=content)
        return {
            "cleaned_content": clean_web_result.model_dump(mode="json"),
            "content_status": "success",
            "cleaned_content_attempts": cleaned_content_attempts,
        }







