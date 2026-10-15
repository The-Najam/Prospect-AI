from research.data_extraction import fetch_all, normalize_deduplicate_links, input_links, fetch_homepage, url_classification
import asyncio
from bs4 import BeautifulSoup
from models.web_extraction_schema import WebExtraction
from config.logger import logger
from models.workflow_state import WorkflowState


def clean_html(state:WorkflowState):
    content = []

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
    state['cleaned_content_attempts'] += 1
    logger.info(f"CLEANING CONTENT ATTEMPT : {state['cleaned_content_attempts']}")
    if not content:
        
        logger.info(" No usable HTML content was fetched. Retrying Again!")
        return {"cleaned_content":content}
        
    else:
        clean_web_result = WebExtraction(pages=content)
        print("Cleaning Content Completed", clean_web_result)
        return {
            "cleaned_content": clean_web_result.model_dump(mode="json"),
            "content_status": "success",
        }


if __name__ == "__main__":
    url = input_links()
    page_content, links  = asyncio.run(fetch_homepage(url))
    urls = normalize_deduplicate_links(links,url)
    selected_pages_url = url_classification(urls)
    selected_pages_url.append({"url":url, "page_type":"Home"})
    page_content = asyncio.run(fetch_all(selected_pages_url))
    content = clean_html(page_content)




