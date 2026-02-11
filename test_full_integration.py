"""
Comprehensive test for Gemini API integration
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_gemini_integration():
    """Test all Gemini API integrations"""
    from app.utils.gemini_client import gemini_client
    from app.agents.research_agent import research_agent
    from app.agents.qualification_agent import qualification_agent
    from app.config import settings
    
    print("=" * 70)
    print("🧪 COMPREHENSIVE GEMINI API TEST")
    print("=" * 70)
    
    # Test 1: Configuration
    print("\n📋 Test 1: Configuration")
    print("-" * 70)
    print(f"✓ API Key: {settings.GEMINI_API_KEY[:20]}...{settings.GEMINI_API_KEY[-10:]}")
    print(f"✓ Model: {settings.GEMINI_MODEL}")
    print(f"✓ Temperature: {settings.GEMINI_TEMPERATURE}")
    print(f"✓ Max Tokens: {settings.GEMINI_MAX_TOKENS}")
    
    # Test 2: Basic Generation
    print("\n📝 Test 2: Basic Text Generation")
    print("-" * 70)
    try:
        response = await gemini_client.generate(
            "Say 'API is working!' in Arabic",
            temperature=0.7
        )
        print(f"✅ Response: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 3: JSON Generation
    print("\n🔧 Test 3: JSON Generation")
    print("-" * 70)
    try:
        json_response = await gemini_client.generate_json(
            "Generate a JSON object with keys 'status' and 'message'. Status should be 'success'."
        )
        print(f"✅ JSON Response: {json_response}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 4: Qualification Agent
    print("\n🎯 Test 4: Qualification Agent")
    print("-" * 70)
    try:
        test_lead = {
            "company_name": "TechCorp Inc",
            "industry": "Software",
            "company_size": "50-200",
            "location": "San Francisco",
            "description": "Leading SaaS company specializing in AI solutions"
        }
        criteria = {
            "target_industry": "Software",
            "min_company_size": 50,
            "budget_range": "high"
        }
        
        score_result = await qualification_agent.score_lead(test_lead, criteria)
        print(f"✅ Score: {score_result['score']:.2f}")
        print(f"✅ Quality: {score_result['quality']}")
        print(f"✅ Reasoning: {score_result['reasoning'][:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 5: Research Agent (Search Queries)
    print("\n🔍 Test 5: Research Agent - Query Generation")
    print("-" * 70)
    try:
        state = {
            "industry": "Technology",
            "location": "USA",
            "company_size": "50-200"
        }
        result_state = await research_agent.generate_search_queries(state)
        queries = result_state.get("search_queries", [])
        print(f"✅ Generated {len(queries)} queries:")
        for i, query in enumerate(queries[:3], 1):
            print(f"   {i}. {query}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✨ ALL TESTS PASSED! Gemini API is fully integrated and working!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = asyncio.run(test_gemini_integration())
    sys.exit(0 if success else 1)
