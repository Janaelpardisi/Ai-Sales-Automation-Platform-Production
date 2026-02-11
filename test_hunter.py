"""
Test Hunter.io API integration
"""
import asyncio
import sys
sys.path.insert(0, 'backend')

from app.tools.email_finder import email_finder

async def test_hunter():
    print("=" * 60)
    print("🔍 TESTING HUNTER.IO API")
    print("=" * 60)
    
    # Test domains
    test_cases = [
        {"domain": "stripe.com", "company": "Stripe"},
        {"domain": "google.com", "company": "Google"},
        {"domain": "github.com", "company": "GitHub"},
    ]
    
    for test in test_cases:
        print(f"\n📧 Searching emails for: {test['company']} ({test['domain']})")
        
        email = await email_finder.find_email_hunter(
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
    asyncio.run(test_hunter())
