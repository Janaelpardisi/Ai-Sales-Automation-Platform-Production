"""
Schemas Package
"""

from app.schemas.campaign import (
    Campaign,
    CampaignCreate,
    CampaignList,
    CampaignStats,
    CampaignUpdate,
)
from app.schemas.email import Email, EmailCreate, EmailList, EmailUpdate
from app.schemas.lead import Lead, LeadCreate, LeadList, LeadUpdate

__all__ = [
    "Campaign",
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignList",
    "CampaignStats",
    "Lead",
    "LeadCreate",
    "LeadUpdate",
    "LeadList",
    "Email",
    "EmailCreate",
    "EmailUpdate",
    "EmailList",
]