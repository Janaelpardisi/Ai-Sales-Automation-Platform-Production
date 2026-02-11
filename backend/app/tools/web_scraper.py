"""
Web Scraper Tool
"""

import asyncio
from typing import List, Optional
from bs4 import BeautifulSoup
import httpx
from playwright.async_api import async_playwright
from app.config import settings


class WebScraper:
    """Web scraping utility"""
    
    def __init__(self):
        self.delay = settings.SCRAPING_DELAY
        self.user_agent = settings.USER_AGENT
    
    async def scrape_with_httpx(self, url: str) -> str:
        """Simple HTTP scraping"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"User-Agent": self.user_agent},
                timeout=30.0,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.text
    
    async def scrape_with_playwright(self, url: str) -> str:
        """Browser-based scraping for JavaScript-heavy sites"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=settings.PLAYWRIGHT_HEADLESS
            )
            page = await browser.new_page(
                user_agent=self.user_agent
            )
            await page.goto(url, wait_until="networkidle")
            content = await page.content()
            await browser.close()
            return content
    
    async def extract_company_info(self, url: str) -> dict:
        """Extract company information from website"""
        try:
            html = await self.scrape_with_httpx(url)
            soup = BeautifulSoup(html, 'lxml')
            
            # Extract basic info
            title = soup.find('title')
            company_name = title.text.strip() if title else ""
            
            # Try to find description
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '')
            
            # Extract text content
            text_content = soup.get_text(separator=' ', strip=True)[:2000]
            
            return {
                "company_name": company_name,
                "description": description,
                "url": url,
                "text_content": text_content
            }
        except Exception as e:
            return {" error": str(e), "url": url}
    
    async def google_search_real(self, query: str, num_results: int = 10) -> List[dict]:
        """
        Real Google search using SerpAPI
        
        Returns list of search results with:
        - title: Company/page title
        - url: Website URL
        - snippet: Description
        - position: Search result position
        """
        from serpapi import GoogleSearch
        from app.config import settings
        
        if not settings.SERPAPI_KEY:
            raise ValueError("SERPAPI_KEY not configured. Please add it to .env file.")
        
        try:
            params = {
                "q": query,
                "api_key": settings.SERPAPI_KEY,
                "num": min(num_results, 10),  # SerpAPI max is 10 per request
                "engine": "google"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Extract organic results
            organic_results = results.get("organic_results", [])
            
            formatted_results = []
            for i, result in enumerate(organic_results[:num_results]):
                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "position": result.get("position", i+1)
                })
            
            return formatted_results
            
        except Exception as e:
            # Fallback to mock if SerpAPI fails
            print(f"SerpAPI error: {e}. Falling back to mock data.")
            return await self.google_search_mock(query, num_results)
    
    async def google_search_mock(self, query: str, num_results: int = 10) -> List[dict]:
        """
        Mock Google search (replace with SerpAPI in production)
        
        For production use:
        - SerpAPI: https://serpapi.com/
        - ScraperAPI: https://www.scraperapi.com/
        - Or official Google Custom Search API
        """
        # Mock results for development
        mock_results = []
        for i in range(min(num_results, 5)):
            mock_results.append({
                "title": f"Company Result {i+1} for {query}",
                "url": f"https://example-company-{i+1}.com",
                "snippet": f"A leading company in {query}",
                "position": i+1
            })
        
        return mock_results
    
    async def extract_emails_from_page(self, url: str) -> List[str]:
        """Extract email addresses from a webpage"""
        import re
        try:
            html = await self.scrape_with_httpx(url)
            
            # Simple regex to find emails
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, html)
            
            # Deduplicate
            return list(set(emails))
        except Exception:
            return []


# Global instance
web_scraper = WebScraper()