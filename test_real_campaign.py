"""
Test Real Campaign with SerpAPI
"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("🧪 TESTING REAL CAMPAIGN WITH SERPAPI")
print("=" * 60)

# Create campaign
print("\n1️⃣ Creating campaign for 'SaaS in USA'...")
campaign_data = {
    "name": "Real SaaS USA Campaign",
    "description": "Testing with REAL Google search via SerpAPI",
    "target_criteria": {
        "industry": "SaaS",
        "location": "USA",
        "company_size": "50-200"
    },
    "email_template": "initial",
    "status": "draft"
}

response = requests.post(f"{BASE_URL}/campaigns", json=campaign_data)
if response.status_code in [200, 201]:
    campaign = response.json()
    campaign_id = campaign["id"]
    print(f"✅ Campaign created: ID={campaign_id}")
else:
    print(f"❌ Failed: {response.status_code}")
    exit(1)

# Run campaign (will use SerpAPI if USE_REAL_SEARCH=True)
print(f"\n2️⃣ Running campaign {campaign_id}...")
print("⏳ This will use REAL Google search via SerpAPI...")

response = requests.post(f"{BASE_URL}/campaigns/{campaign_id}/run")
if response.status_code == 200:
    result = response.json().get('data', response.json())
    print(f"✅ Campaign completed!")
    print(f"   Leads found: {result.get('leads_found', 0)}")
    print(f"   Leads created: {result.get('leads_created', 0)}")
else:
    print(f"❌ Failed: {response.status_code}")
    print(response.text)
    exit(1)

# Check leads
print(f"\n3️⃣ Checking leads...")
response = requests.get(f"{BASE_URL}/leads/?campaign_id={campaign_id}")
if response.status_code == 200:
    data = response.json()
    leads = data['items']
    print(f"✅ Found {len(leads)} leads:\n")
    
    for lead in leads[:5]:  # Show first 5
        print(f"Company: {lead['company_name']}")
        print(f"Website: {lead['company_website']}")
        print(f"Industry: {lead['industry']}")
        print(f"Location: {lead['location']}")
        print(f"Source: {lead['source']}")
        print(f"---")

print("\n" + "=" * 60)
print("✨ TEST COMPLETE!")
print("=" * 60)
