"""
Quick test to check if USE_REAL_SEARCH is loaded correctly
"""
import sys
sys.path.insert(0, 'backend')

from app.config import settings

print("=" * 60)
print("🔍 CHECKING CONFIGURATION")
print("=" * 60)

print(f"\nSERPAPI_KEY: {settings.SERPAPI_KEY[:20]}..." if settings.SERPAPI_KEY else "SERPAPI_KEY: NOT SET")
print(f"USE_REAL_SEARCH: {settings.USE_REAL_SEARCH}")
print(f"USE_REAL_EMAILS: {settings.USE_REAL_EMAILS}")

print("\n" + "=" * 60)

if settings.USE_REAL_SEARCH:
    print("✅ Real search is ENABLED")
else:
    print("❌ Real search is DISABLED - using mock data")

print("=" * 60)
