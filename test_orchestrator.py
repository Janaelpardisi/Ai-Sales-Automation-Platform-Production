"""
Direct test of orchestrator agent with SerpAPI
"""
import asyncio
import sys
sys.path.insert(0, 'backend')

from app.agents.orchestrator import orchestrator_agent

async def test_orchestrator():
    print("=" * 60)
    print("🧪 TESTING ORCHESTRATOR AGENT DIRECTLY")
    print("=" * 60)
    
    criteria = {
        "industry": "SaaS",
        "location": "USA",
        "company_size": "50-200",
        "email_template": "initial"
    }
    
    print(f"\n📋 Criteria: {criteria}")
    print("\n⏳ Running orchestrator...")
    
    try:
        qualified_leads = await orchestrator_agent.run_campaign(criteria)
        print(f"\n✅ SUCCESS! Found {len(qualified_leads)} qualified leads:\n")
        
        for i, lead in enumerate(qualified_leads[:3], 1):
            print(f"{i}. {lead.get('company_name', 'Unknown')}")
            print(f"   Website: {lead.get('website', 'N/A')}")
            print(f"   Industry: {lead.get('industry', 'N/A')}")
            print(f"   Location: {lead.get('location', 'N/A')}")
            print(f"   Source: {lead.get('source', 'N/A')}")
            print()
        
    except Exception as e:
        print(f"\n❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
