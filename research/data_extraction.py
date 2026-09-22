from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter
import asyncio
from bs4 import BeautifulSoup
from config.logger import logger


url_filter = URLPatternFilter(patterns=[
    "*about*",
    "*service*",
    "*portfolio*",
    "*case-study*"
]
)
config = CrawlerRunConfig(
    deep_crawl_strategy=BFSDeepCrawlStrategy(
        max_depth=0,
        max_pages=10,
        include_external=False,
        filter_chain=FilterChain([url_filter])

    )
)


async def main():
    try:
        async with AsyncWebCrawler() as crawler:
            content = await crawler.arun("https://creatifsoft.com/", config=config)
            page_content = []

            for c in content:
                url = c.url
                page_content.append({"url":url, "html":c.cleaned_html})
                
        logger.info("Websites Pages Extracted Successfully")
        return page_content
    except Exception as e:
        logger.error("Failed To Extract Pages!", e)

        
            
        
        
        
    



if __name__ == "__main__":

    page_content = asyncio.run(main())











