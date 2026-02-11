"""
Test script for Gemini API key
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    
    # Load environment variables
    env_path = backend_path / ".env"
    load_dotenv(env_path)
    
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    print("=" * 60)
    print("🔑 Testing Gemini API Key")
    print("=" * 60)
    print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    print(f"Model: {model_name}")
    print("-" * 60)
    
    # Configure API
    genai.configure(api_key=api_key)
    
    # Create model
    model = genai.GenerativeModel(model_name)
    
    # Test with a simple prompt
    print("\n📝 Sending test prompt...")
    response = model.generate_content("Say 'Hello! The API key is working perfectly!' in Arabic")
    
    print("\n✅ Response received:")
    print("-" * 60)
    print(response.text)
    print("-" * 60)
    
    print("\n✨ SUCCESS! API key is working correctly!")
    print("=" * 60)
    
except Exception as e:
    print("\n❌ ERROR!")
    print("=" * 60)
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print("=" * 60)
    sys.exit(1)
