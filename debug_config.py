"""
Debug configuration loading
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.config import settings
from dotenv import load_dotenv
import os

print("=" * 70)
print("🔍 CONFIGURATION DEBUG")
print("=" * 70)

# Check .env file
env_path = backend_path / ".env"
print(f"\n📁 .env file path: {env_path}")
print(f"📁 .env exists: {env_path.exists()}")

if env_path.exists():
    print(f"\n📄 .env file contents:")
    print("-" * 70)
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if 'GEMINI_API_KEY' in line:
                # Mask the key for security
                parts = line.split('=')
                if len(parts) == 2:
                    key = parts[1].strip()
                    print(f"GEMINI_API_KEY={key[:20]}...{key[-10:]}")
            elif 'GEMINI' in line:
                print(line.strip())

# Load .env manually
print(f"\n🔄 Loading .env manually...")
load_dotenv(env_path)

print(f"\n📋 Environment Variables:")
print("-" * 70)
print(f"GEMINI_API_KEY from os.getenv: {os.getenv('GEMINI_API_KEY', 'NOT FOUND')[:30]}...")
print(f"GEMINI_MODEL from os.getenv: {os.getenv('GEMINI_MODEL', 'NOT FOUND')}")

print(f"\n⚙️ Settings Object:")
print("-" * 70)
print(f"settings.GEMINI_API_KEY: {settings.GEMINI_API_KEY[:30] if settings.GEMINI_API_KEY else 'EMPTY'}...")
print(f"settings.GEMINI_MODEL: {settings.GEMINI_MODEL}")
print(f"settings.GEMINI_TEMPERATURE: {settings.GEMINI_TEMPERATURE}")
print(f"settings.GEMINI_MAX_TOKENS: {settings.GEMINI_MAX_TOKENS}")

print("\n" + "=" * 70)
