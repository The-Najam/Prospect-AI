
# importing Libraries
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from models.web_extraction_schema import WebExtraction
from config.logger import logger
from urllib.parse import urlparse, urljoin, urlsplit, urlunsplit
from bs4 import BeautifulSoup
import socket
from models.workflow_state import WorkflowState
from langsmith import traceable
import json
import requests
import ipaddress


def validate_prospect_url(url: str) -> None:
    """Reject URLs that cannot be used as a prospect website."""
    try:
        parsed_url = urlsplit(url)
        hostname = parsed_url.hostname
    except ValueError as exc:
        raise ValueError("The URL is malformed.") from exc

    if parsed_url.scheme not in {"http", "https"} or not hostname:
        raise ValueError("Enter a complete HTTP or HTTPS website URL.")

    try:
        is_ip_address = ipaddress.ip_address(hostname) is not None
    except ValueError:
        is_ip_address = False

    if hostname != "localhost" and not is_ip_address and "." not in hostname:
        raise ValueError("Enter a complete website domain, such as example.com.")

    hostname = hostname.lower()
    path = parsed_url.path.lower()
    image_extensions = (
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".tif", ".tiff"
    )
    is_image_host = (
        hostname.startswith("encrypted-tbn") and hostname.endswith(".gstatic.com")
    )
    if path.endswith(image_extensions) or is_image_host:
        raise ValueError("Image URLs are not supported. Enter the prospect website URL.")



# Get Prospect Link and validate url
def input_links(state:WorkflowState):
    
    url = input("Paste the url of Prospect Website : ")
    validate_prospect_url(url)
    state['prospect_url'] = url

    if url.startswith(("http://","https://")):
            domain = urlparse(url).netloc
            try:
                print(socket.gethostbyname(domain))
                logger.info("Valid Reachable Domain")
            except socket.gaierror:
                logger.error("Domain Not Exist")

            try:      
                response = requests.get(url, timeout=10)
                logger.info("Server is reachable")
                logger.info("Status:", response.status_code)
                return {"prospect_url":url}
            
            except requests.exceptions.RequestException as e:
                logger.error("Server could not be reached", e)
    else:
        logger.error("Invalid Url")


# Fetch Homepage and Extract Links from Prospect's Website
async def fetch_homepage(state:WorkflowState):
    url = state['prospect_url']
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
        state['page_content'] = page_content
        state['links'] = links

        return {"page_content":page_content, "links": links}
    

# Normalize and Deduplicate Links
def normalize_deduplicate_links(state:WorkflowState):
    homepage_url = state['prospect_url']
    absolute_links = [urljoin(homepage_url, link) for link in state['links']]
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
    main_url_parts = urlsplit(state['prospect_url'])
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

    return {"links":unique_urls}


# classify url based on categories and fetch only Four
def url_classification(state: WorkflowState):
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
    max_pages = 4
    links = state.get("links", [])

    for url in links:
        parts = urlsplit(url)
        segments = parts.path.strip("/").lower().split("/")

        for segment in segments:
            for page_type, keywords in page_keywords.items():
                if segment in keywords:
                    selected_page_type.append({
                        "url": url,
                        "page_type": page_type
                    })
                    break

            # Stop once we have selected 4 pages
            if len(selected_page_type) >= max_pages:
                break

        if len(selected_page_type) >= max_pages:
            break

    selected_page_type.append({"url":state["prospect_url"], "page_type":"Home"})
    state["page_content"] = selected_page_type

    return {"page_content": selected_page_type}



@traceable(run_type="tool", name="crawl_page")
async def fetch_all(state:WorkflowState):
    page_content = []
    config = CrawlerRunConfig(
    page_timeout=15_000
)
    # fetching important urls content
    async with AsyncWebCrawler() as crawler:
        for page in state['page_content']:
            url = page["url"]
            page_type = page["page_type"]
            if url.lower().endswith((
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".webp",
                ".svg",
                ".css",
                ".js",
                ".mp4",
                ".mp3",
                ".zip"
            )):
                logger.info("This URL points to a non-data file")
                continue
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
                    
    return {"page_content":page_content}




