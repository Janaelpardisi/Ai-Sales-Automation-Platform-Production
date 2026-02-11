"""
Test Snov.io API integration
"""
import asyncio
import sys
sys.path.insert(0, 'backend')

from app.tools.email_finder import email_finder

async def test_snov():
    print("=" * 60)
    print("🔍 TESTING SNOV.IO API")
    print("=" * 60)
    
    # Test domains
    test_cases = [
        {"domain": "stripe.com", "company": "Stripe"},
        {"domain": "github.com", "company": "GitHub"},
        {"domain": "shopify.com", "company": "Shopify"},
    ]
    
    for test in test_cases:
        print(f"\n📧 Searching emails for: {test['company']} ({test['domain']})")
        
        email = await email_finder.find_email_snov(
            domain=test['domain'],
            company_name=test['company']
        )
        
        if email:
            print(f"   ✅ Found: {email}")
        else:
            print(f"   ❌ No email found")
    
    print("\n" + "=" * 60)
    print("✨ TEST COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_snov())
