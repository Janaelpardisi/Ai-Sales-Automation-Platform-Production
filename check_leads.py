"""
Quick check for campaign 18 leads location
"""
import requests

response = requests.get("http://localhost:8000/api/v1/leads/?campaign_id=18")
data = response.json()

print(f"Total leads: {data['total']}\n")

for lead in data['items']:
    print(f"Company: {lead['company_name']}")
    print(f"Industry: {lead['industry']}")
    print(f"Location: {lead['location']}")
    print(f"---")
