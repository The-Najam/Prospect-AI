from research.data_extraction import fetch_all, normalize_deduplicate_links, input_links, fetch_homepage, url_classification
import asyncio
from bs4 import BeautifulSoup
from models.web_extraction_schema import WebExtraction
from config.logger import logger


def clean_html(page_content):
    content = []

    for page in page_content:
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

    if not content:
        raise ValueError("No usable HTML content was fetched")

    clean_web_result = WebExtraction(pages=content)
    print("Cleaning Content Completed", clean_web_result)
    print(type(clean_web_result))
    return clean_web_result


if __name__ == "__main__":
    url = input_links()
    page_content, links  = asyncio.run(fetch_homepage(url))
    urls = normalize_deduplicate_links(links,url)
    selected_pages_url = url_classification(urls)
    selected_pages_url.append({"url":url, "page_type":"Home"})
    page_content = asyncio.run(fetch_all(selected_pages_url))
    content = clean_html(page_content)




