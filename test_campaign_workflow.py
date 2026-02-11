import httpx
import asyncio
import json

async def test_campaign():
    """Test creating and running a campaign"""
    base_url = "http://localhost:8000/api/v1"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. Create a new campaign
        print("📝 Creating test campaign...")
        campaign_data = {
            "name": "GitHub Test Campaign",
            "description": "Testing campaign functionality before GitHub push",
            "target_criteria": {
                "industry": "Technology",
                "location": "USA",
                "company_size": "10-50"
            }
        }
        
        response = await client.post(f"{base_url}/campaigns/", json=campaign_data)
        print(f"✅ Campaign created: {response.status_code}")
        campaign = response.json()
        print(f"   Campaign ID: {campaign['id']}")
        print(f"   Campaign Name: {campaign['name']}")
        
        # 2. Run the campaign
        print(f"\n🚀 Running campaign {campaign['id']}...")
        response = await client.post(f"{base_url}/campaigns/{campaign['id']}/run")
        print(f"✅ Campaign run: {response.status_code}")
        result = response.json()
        print(f"\n📊 Results:")
        print(f"   Leads found: {result.get('data', {}).get('leads_found', 0)}")
        print(f"   Leads created: {result.get('data', {}).get('leads_created', 0)}")
        print(f"   Emails sent: {result.get('data', {}).get('emails_sent', 0)}")
        print(f"   Emails failed: {result.get('data', {}).get('emails_failed', 0)}")
        
        # 3. Get campaign stats
        print(f"\n📈 Getting campaign statistics...")
        response = await client.get(f"{base_url}/campaigns/{campaign['id']}/stats")
        stats = response.json()
        print(f"   Total leads: {stats.get('total_leads', 0)}")
        print(f"   Qualified leads: {stats.get('qualified_leads', 0)}")
        print(f"   Emails sent: {stats.get('emails_sent', 0)}")
        
        # 4. List all campaigns
        print(f"\n📋 Listing all campaigns...")
        response = await client.get(f"{base_url}/campaigns/")
        campaigns = response.json()
        print(f"   Total campaigns: {campaigns.get('total', 0)}")
        
        print("\n✅ All tests passed!")
        return True

if __name__ == "__main__":
    asyncio.run(test_campaign())
