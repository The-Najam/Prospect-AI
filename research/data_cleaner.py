from research.data_extraction import main
import asyncio
from bs4 import BeautifulSoup

def clean_html(page_content):
    content = []
    for page in page_content:
        url = page["url"]
        html = page["html"]
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["header", "nav", "footer", "script", "style"]):
            tag.decompose()

        cont = soup.get_text(" ", strip=True)
        content.append({"url":url, "page_content":cont})


    print(type(content))

    return content


if __name__ == "__main__":
    page_content = asyncio.run(main())
    content = clean_html(page_content)



