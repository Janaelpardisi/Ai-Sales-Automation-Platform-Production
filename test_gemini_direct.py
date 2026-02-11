"""
Simple Gemini API test - Direct testing without agents
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_gemini_direct():
    """Test Gemini API directly"""
    from app.utils.gemini_client import gemini_client
    from app.config import settings
    
    print("=" * 70)
    print("🧪 DIRECT GEMINI API TEST")
    print("=" * 70)
    
    # Test 1: Configuration
    print("\n📋 Test 1: Configuration Check")
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
            "قول 'مرحباً! الـ API شغال تمام!' بالعربي",
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
            """Generate a JSON object with the following structure:
            {
                "status": "success",
                "message": "API is working perfectly",
                "test_number": 3,
                "features": ["text generation", "json parsing", "async support"]
            }"""
        )
        print(f"✅ JSON Response:")
        import json
        print(json.dumps(json_response, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 4: Lead Scoring Simulation
    print("\n🎯 Test 4: Lead Scoring Simulation")
    print("-" * 70)
    try:
        prompt = """
You are a B2B lead qualification expert. Score this lead from 0.0 to 1.0.

LEAD INFORMATION:
- Company: TechCorp Inc
- Industry: Software
- Size: 100 employees
- Location: San Francisco
- Description: Leading SaaS company specializing in AI solutions

Provide a JSON response with:
{
    "score": 0.0-1.0,
    "quality": "hot" | "warm" | "cold",
    "reasoning": "explanation"
}
"""
        result = await gemini_client.generate_json(prompt)
        print(f"✅ Score: {result.get('score', 'N/A')}")
        print(f"✅ Quality: {result.get('quality', 'N/A')}")
        print(f"✅ Reasoning: {result.get('reasoning', 'N/A')[:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 5: Search Query Generation
    print("\n🔍 Test 5: Search Query Generation")
    print("-" * 70)
    try:
        prompt = """
Generate 5 specific search queries to find companies matching these criteria:
- Industry: Technology
- Location: USA
- Company Size: 50-200

Return as JSON array of strings.
Example: ["SaaS companies in San Francisco", "fintech startups in NYC"]
"""
        queries = await gemini_client.generate_json(prompt)
        print(f"✅ Generated {len(queries) if isinstance(queries, list) else 0} queries:")
        if isinstance(queries, list):
            for i, query in enumerate(queries[:3], 1):
                print(f"   {i}. {query}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✨ ALL TESTS PASSED! Gemini API is fully functional!")
    print("=" * 70)
    print("\n💡 Next Steps:")
    print("   1. API key is configured correctly")
    print("   2. All API functions are working")
    print("   3. Ready to use in the application")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = asyncio.run(test_gemini_direct())
    sys.exit(0 if success else 1)
