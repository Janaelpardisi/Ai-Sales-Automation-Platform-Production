"""
Test Email Sending - Simple Test
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_create_and_run_campaign():
    """Create a campaign and test email sending"""
    
    print("=" * 60)
    print("🧪 TESTING EMAIL SYSTEM")
    print("=" * 60)
    
    # 1. Create Campaign
    print("\n1️⃣ Creating campaign...")
    campaign_data = {
        "name": "Email Test Campaign",
        "description": "Testing email sending with Outlook",
        "target_criteria": {
            "industry": "Technology",
            "location": "Egypt",
            "company_size": "10-50"
        },
        "email_template": "initial",
        "status": "draft"
    }
    
    response = requests.post(f"{BASE_URL}/campaigns", json=campaign_data)
    if response.status_code in [200, 201]:
        campaign = response.json()
        campaign_id = campaign["id"]
        print(f"✅ Campaign created: ID={campaign_id}, Name='{campaign['name']}'")
    else:
        print(f"❌ Failed to create campaign: {response.status_code}")
        print(response.text)
        return
    
    # 2. Run Campaign (this will send emails!)
    print(f"\n2️⃣ Running campaign {campaign_id}...")
    print("⏳ This will:")
    print("   - Generate mock leads")
    print("   - Find contact emails")
    print("   - Send personalized emails")
    print("   - Track results")
    print()
    
    response = requests.post(f"{BASE_URL}/campaigns/{campaign_id}/run")
    if response.status_code == 200:
        response_data = response.json()
        # Extract the actual result from the wrapped response
        result = response_data.get('data', response_data)
        print("✅ Campaign completed!")
        print(f"\n📊 Results:")
        print(f"   • Leads found: {result.get('leads_found', 0)}")
        print(f"   • Leads created: {result.get('leads_created', 0)}")
        print(f"   • Emails sent: {result.get('emails_sent', 0)}")
        print(f"   • Emails failed: {result.get('emails_failed', 0)}")
    else:
        print(f"❌ Failed to run campaign: {response.status_code}")
        print(response.text)
        return
    
    # 3. Get Analytics
    print(f"\n3️⃣ Getting email analytics...")
    response = requests.get(f"{BASE_URL}/analytics/campaigns/{campaign_id}/email-stats")
    if response.status_code == 200:
        stats = response.json()
        print("✅ Email Statistics:")
        print(f"   • Total leads: {stats.get('total_leads', 0)}")
        print(f"   • Emails sent: {stats.get('emails_sent', 0)}")
        print(f"   • Open rate: {stats.get('open_rate', 0)}%")
        print(f"   • Click rate: {stats.get('click_rate', 0)}%")
        print(f"   • Reply rate: {stats.get('reply_rate', 0)}%")
    else:
        print(f"⚠️  Analytics not available: {response.status_code}")
    
    # 4. List Leads
    print(f"\n4️⃣ Listing campaign leads...")
    response = requests.get(f"{BASE_URL}/leads?campaign_id={campaign_id}")
    if response.status_code == 200:
        leads = response.json()
        print(f"✅ Found {len(leads)} leads:")
        for i, lead in enumerate(leads[:3], 1):  # Show first 3
            print(f"\n   Lead {i}:")
            print(f"   • Company: {lead.get('company_name', 'N/A')}")
            print(f"   • Email: {lead.get('contact_email', 'N/A')}")
            print(f"   • Status: {lead.get('status', 'N/A')}")
            print(f"   • Emails sent: {lead.get('emails_sent', 0)}")
    
    print("\n" + "=" * 60)
    print("✨ TEST COMPLETE!")
    print("=" * 60)
    print("\n📧 Check your Outlook inbox for test emails!")
    print("   (They might be in Sent folder)")
    print()


if __name__ == "__main__":
    try:
        test_create_and_run_campaign()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server!")
        print("   Make sure the server is running: python -m app.main")
    except Exception as e:
        print(f"❌ Error: {e}")
