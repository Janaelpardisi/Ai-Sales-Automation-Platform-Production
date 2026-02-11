"""
Test the AI Sales Agent API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("🧪 AI SALES AGENT API TEST")
print("=" * 70)

# Test 1: Health Check
print("\n📋 Test 1: Health Check")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Create Campaign
print("\n📝 Test 2: Create Campaign")
print("-" * 70)
try:
    campaign_data = {
        "name": "Test Campaign - Tech Companies",
        "description": "Testing the AI Sales Agent with tech companies",
        "target_criteria": {
            "industry": "Technology",
            "location": "USA",
            "company_size": "50-200"
        },
        "email_template": "Hi {contact_name}, I noticed {company_name}...",
        "subject_template": "Quick question about {company_name}",
        "follow_up_enabled": True,
        "max_follow_ups": 2,
        "daily_limit": 10,
        "total_limit": 50
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/campaigns/",
        json=campaign_data
    )
    print(f"✅ Status: {response.status_code}")
    campaign = response.json()
    print(f"✅ Campaign ID: {campaign['id']}")
    print(f"✅ Campaign Name: {campaign['name']}")
    print(f"✅ Status: {campaign['status']}")
    
    campaign_id = campaign['id']
except Exception as e:
    print(f"❌ Error: {e}")
    campaign_id = None

# Test 3: List Campaigns
print("\n📋 Test 3: List Campaigns")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/v1/campaigns/")
    print(f"✅ Status: {response.status_code}")
    data = response.json()
    print(f"✅ Total Campaigns: {data['total']}")
    for camp in data['items']:
        print(f"   - {camp['name']} (ID: {camp['id']}, Status: {camp['status']})")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Get Campaign Details
if campaign_id:
    print(f"\n🔍 Test 4: Get Campaign Details (ID: {campaign_id})")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/api/v1/campaigns/{campaign_id}")
        print(f"✅ Status: {response.status_code}")
        campaign = response.json()
        print(f"✅ Name: {campaign['name']}")
        print(f"✅ Description: {campaign['description']}")
        print(f"✅ Target Criteria: {json.dumps(campaign['target_criteria'], indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Test 5: Run Campaign
if campaign_id:
    print(f"\n🚀 Test 5: Run Campaign (ID: {campaign_id})")
    print("-" * 70)
    print("⚠️  This will execute the campaign workflow with AI agents...")
    print("⚠️  It may take a few moments...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/campaigns/{campaign_id}/run")
        print(f"✅ Status: {response.status_code}")
        result = response.json()
        print(f"✅ Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Test 6: Get Campaign Stats
if campaign_id:
    print(f"\n📊 Test 6: Get Campaign Stats (ID: {campaign_id})")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/api/v1/campaigns/{campaign_id}/stats")
        print(f"✅ Status: {response.status_code}")
        stats = response.json()
        print(f"✅ Total Leads: {stats['total_leads']}")
        print(f"✅ Qualified Leads: {stats['qualified_leads']}")
        print(f"✅ Emails Sent: {stats['emails_sent']}")
        print(f"✅ Open Rate: {stats['open_rate']:.1%}")
        print(f"✅ Reply Rate: {stats['reply_rate']:.1%}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Test 7: List Leads
print("\n📋 Test 7: List Leads")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/v1/leads/")
    print(f"✅ Status: {response.status_code}")
    data = response.json()
    print(f"✅ Total Leads: {data['total']}")
    for lead in data['items'][:5]:  # Show first 5
        print(f"   - {lead['company_name']} (Quality: {lead['quality']}, Score: {lead['quality_score']:.2f})")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("✨ API TESTING COMPLETE!")
print("=" * 70)
