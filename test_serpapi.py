"""
Test SerpAPI Integration - Real Google Search
"""
import asyncio
from app.tools.web_scraper import web_scraper

async def test_serpapi():
    print("=" * 60)
    print("🧪 TESTING SERPAPI - REAL GOOGLE SEARCH")
    print("=" * 60)
    
    query = "SaaS companies in USA"
    print(f"\n🔍 Searching for: '{query}'")
    print("⏳ Please wait...")
    
    try:
        results = await web_scraper.google_search_real(query, num_results=5)
        
        print(f"\n✅ Found {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Description: {result['snippet'][:100]}...")
            print()
        
        print("=" * 60)
        print("✨ SERPAPI TEST SUCCESSFUL!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPossible issues:")
        print("1. SERPAPI_KEY not configured in .env")
        print("2. Invalid API key")
        print("3. API quota exceeded")

if __name__ == "__main__":
    asyncio.run(test_serpapi())
