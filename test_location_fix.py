"""
Test Location Fix - Create campaign for USA and verify location
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_location_fix():
    print("=" * 60)
    print("🧪 TESTING LOCATION FIX")
    print("=" * 60)
    
    # Create campaign for USA
    print("\n1️⃣ Creating campaign for SaaS in USA...")
    campaign_data = {
        "name": "SaaS USA Test",
        "description": "Testing location fix - should generate USA leads",
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
        print(f"   Target: {campaign['target_criteria']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return
    
    # Run campaign
    print(f"\n2️⃣ Running campaign {campaign_id}...")
    response = requests.post(f"{BASE_URL}/campaigns/{campaign_id}/run")
    if response.status_code == 200:
        result = response.json().get('data', response.json())
        print(f"✅ Campaign completed!")
        print(f"   Leads created: {result.get('leads_created', 0)}")
    else:
        print(f"❌ Failed: {response.status_code}")
        return
    
    # Check leads location
    print(f"\n3️⃣ Checking leads location...")
    response = requests.get(f"{BASE_URL}/leads?campaign_id={campaign_id}")
    if response.status_code == 200:
        leads = response.json()
        print(f"✅ Found {len(leads)} leads:\n")
        
        usa_count = 0
        other_count = 0
        
        for lead in leads:
            location = lead.get('location', 'Unknown')
            company = lead.get('company_name', 'Unknown')
            industry = lead.get('industry', 'Unknown')
            
            if location == "USA":
                usa_count += 1
                print(f"   ✅ {company} - {industry} - {location}")
            else:
                other_count += 1
                print(f"   ❌ {company} - {industry} - {location} (WRONG!)")
        
        print(f"\n📊 Results:")
        print(f"   ✅ USA leads: {usa_count}")
        print(f"   ❌ Other locations: {other_count}")
        
        if other_count == 0:
            print(f"\n🎉 SUCCESS! All leads are from USA!")
        else:
            print(f"\n⚠️  FAILED! Some leads are not from USA")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        test_location_fix()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server!")
        print("   Make sure the server is running")
    except Exception as e:
        print(f"❌ Error: {e}")
