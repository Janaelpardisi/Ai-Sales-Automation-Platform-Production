"""
API V1 Routes
"""

from fastapi import APIRouter
from app.api.v1 import campaigns, leads, unsubscribe, analytics

router = APIRouter()

# Include all route modules
router.include_router(campaigns.router)
router.include_router(leads.router)
router.include_router(unsubscribe.router)
router.include_router(analytics.router)