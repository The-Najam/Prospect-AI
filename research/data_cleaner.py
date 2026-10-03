from research.data_extraction import fetch_all, normalize_deduplicate_links, input_links, fetch_homepage, url_classification
import asyncio
from bs4 import BeautifulSoup
from models.web_extraction_schema import WebExtraction


def clean_html(page_content):
    content = []
    "Cleaning Content Started"
    for page in page_content:
        url = page['url']
        html = page['content']
        page_type = page['page_type']
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["header", "nav", "footer", "script", "style"]):
            tag.decompose()
        cont = soup.get_text(" ", strip=True)
        content.append({"url":url, "page_type":page_type, "content":cont})


    clean_web_result = WebExtraction(pages=content)
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




