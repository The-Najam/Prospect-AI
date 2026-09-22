# from research.data_cleaner import content
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from models.research_tool_schema import Bio_Extractor
import asyncio
import re
import json
from bs4 import BeautifulSoup


async def main():
    config = CrawlerRunConfig(
        exclude_social_media_links=False,
        css_selector="footer",
        excluded_tags = []
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://expando.com.pk/", config=config)


    data = result.__dict__
    print(type(data))
    urls = re.findall(r'https?://[^\s<>"\']+', result.markdown)
    social_domains = (
    'facebook.com',
    'instagram.com',
    'linkedin.com',
    'twitter.com',
    'x.com',
    'tiktok.com',
    'youtube.com',
    'pinterest.com',
    'snapchat.com',
    'reddit.com'
    )
    social_urls = [
    url for url in urls
    if any(domain in url.lower() for domain in social_domains)]

    return social_urls



results = []
async def extraction(social_urls):
    config = CrawlerRunConfig(
        excluded_tags=["nav", "footer"],
        exclude_external_links=True,
        exclude_external_images=True,

    )
    async with AsyncWebCrawler() as crawler:
        for ul in social_urls:
            url = ul
            data = await crawler.arun(url=ul, config=config)
            markdown_content = data.markdown
            cleaned = re.sub(r'https?://\S+|www\.\S+', '', markdown_content)
            platform, bio = extract_platform_and_bio(cleaned)
            results.append(
                Bio_Extractor(
                    url=url,
                    platform=platform,
                    bio=bio,
                    success=bool(bio),
                )
            )
 
        return results



import re

def extract_platform_and_bio(text):

    # Instagram
    instagram = re.search(
        r'##\s+([^\n]+)\n\s*\*\s*\[\d+\s+followers\].*?\n\s*\*\s*\[\d+\s+following\].*?\n',
        text,
        re.IGNORECASE
    )

    if instagram:
        bio = text[instagram.end():]

        # Stop at Instagram content
        stop = re.search(
            r'\n\s*(?:\.\.\.\s*\n\s*more|more\s*\n|\[Posts\]\(|\[Reels\]\(|\[Tagged\]\(|\[!\[Photo by|Link icon)',
            bio,
            re.IGNORECASE
        )

        if stop:
            bio = bio[:stop.start()]

        bio = re.sub(r'\[([^\]]*)\]\([^)]*', r'\1', bio)
        bio = re.sub(r'\]\(', '', bio)

        lines = [x.strip() for x in bio.splitlines() if x.strip()]

        return "Instagram", '\n'.join(lines)

    # Facebook
    if re.search(r'Facebook', text, re.IGNORECASE):
        return "Facebook", None

    # LinkedIn
    if re.search(r'LinkedIn|linkedin', text, re.IGNORECASE):
        return "LinkedIn", None

    return None, None





if __name__ == "__main__":
    social_urls = asyncio.run(main())
    asyncio.run(extraction(social_urls))



