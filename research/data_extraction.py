from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
import asyncio
from config.logger import logger
from urllib.parse import urlparse, urljoin, urlsplit, urlunsplit
from bs4 import BeautifulSoup



async def fetch_homepage(url):
    # creating crawler for home page
    async with AsyncWebCrawler() as crawler:
        content = await crawler.arun(url)
        page_content = []

        for c in content:
            url = c.url
            page_content.append({"url":url, "html":c.cleaned_html})

        
        # extracting Links from the homepage 
        soup = BeautifulSoup(content.html, "lxml")
        links = [a.get("href") for a in soup.find_all("a", href=True)]

        return page_content, links
    


def normalize_deduplicate_links(links, url):
    homepage_url = url
    absolute_links = [urljoin(homepage_url, link) for link in links]
    normalize_links = []

    # normalizing links into consisting format
    for link in absolute_links:
        parts = urlsplit(link)

        scheme = parts.scheme.lower()
        hostname = parts.hostname.lower() if parts.hostname else ""

        netloc = hostname
        if parts.port:
            netloc += f":{parts.port}"

        path = parts.path or "/"

        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")

        normalize_links.append(urlunsplit((scheme, netloc, path, parts.query, "")))

    # Performing deduplication
    unique_urls = set(normalize_links) 
    main_url_parts = urlsplit(url)
    company_hostname = main_url_parts.hostname


    #Filtering Http / Https links
    for link in list(unique_urls):
        parts = urlsplit(link)
        if parts.scheme == "https" or parts.scheme == "http":
            if parts.hostname == company_hostname:
                continue
            else:
                unique_urls.remove(link)
        else:
            unique_urls.remove(link)

    return unique_urls



def url_classification(unique_urls):
    page_keywords = {
    "about": ["about", "company", "who-we-are", "our-story"],
    "pricing": ["pricing", "plans", "packages", "rates"],
    "services": ["service", "services", "solutions", "offerings"],
    "contact": ["contact", "contact-us", "get-in-touch", "reach-us"],
    "portfolio": ["portfolio", "projects", "work", "case-studies", "case-study"],
    "testimonials": ["testimonial", "testimonials", "reviews", "customer-reviews"],
    "product": ["product", "products", "platform", "software"],
    "team": ["team", "our-team", "leadership", "people", "management"],
}
    selected_page_type = []

    # mapping urls with page_keywords
    for ur in unique_urls:
        parts = urlsplit(ur)
        path = parts.path
        segments = parts.path.split("/")
        for segment in segments:
            if segment:
                for page_type, keywords in page_keywords.items():
                    if segment.lower() in keywords:
                        if len(selected_page_type) < 4:
                            selected_page_type.append({"url":ur, "page_type":page_type})
                        else:
                            break
                    
            else:
                continue


    return selected_page_type

    
async def fetch_all(selected_page_url):
    page_content = []
    config = CrawlerRunConfig(
    page_timeout=15_000
)
    # fetching important urls content
    async with AsyncWebCrawler() as crawler:
        for page in selected_page_url:
            url = page["url"]
            page_type = page["page_type"]
            try:
                content = await crawler.arun(url,config)
                for c in content:
                    page_content.append({"url":url,"page_type":page_type,"content":c.cleaned_html})
                logger.info(f"Successfully Fetch {page_type} Page")
            except Exception as e:
                    logger.error(
                        f"Failed To Fetch {page_type} Page: {url} — {e}",
                        exc_info=True
                    )

    return page_content


    




if __name__ == "__main__":
    url = "https://prodigmar.com/?gad_source=1&gad_campaignid=23460421827&gbraid=0AAAAABmXAZdfNYGMIldoHkx-SPV0bcUn2&gclid=Cj0KCQjwlNPVBhCMARIsAPZ5Rqje_k3eIL_58vTjo7-NmVn2SED5brQnblnOiihT6j-40DK3Iz_vCZQaAtgdEALw_wcB"
    page_content, links  = asyncio.run(fetch_homepage(url))
    urls = normalize_deduplicate_links(links,url)
    selected_pages_url = url_classification(urls)
    selected_pages_url.append({"url":url, "page_type":"Home"})
    page_content = asyncio.run(fetch_all(selected_pages_url))

