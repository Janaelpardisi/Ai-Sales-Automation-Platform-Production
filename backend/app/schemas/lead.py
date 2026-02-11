"""
Lead Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class LeadBase(BaseModel):
    """Base lead schema"""
    company_name: str = Field(..., min_length=1, max_length=255)
    company_website: Optional[str] = None
    company_domain: Optional[str] = None
    company_linkedin: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    contact_linkedin: Optional[str] = None


class LeadCreate(LeadBase):
    """Schema for creating a lead"""
    campaign_id: Optional[int] = None
    source: Optional[str] = None
    tags: Optional[list[str]] = []


class LeadUpdate(BaseModel):
    """Schema for updating a lead"""
    company_name: Optional[str] = None
    company_website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    status: Optional[str] = None
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    quality: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    is_active: Optional[bool] = None


class Lead(LeadBase):
    """Schema for reading a lead"""
    id: int
    campaign_id: Optional[int]
    quality_score: Optional[float]
    quality: Optional[str]
    status: str
    enrichment_data: dict
    emails_sent: int
    emails_opened: int
    emails_clicked: int
    emails_replied: int
    last_contacted_at: Optional[datetime]
    last_responded_at: Optional[datetime]
    next_follow_up_at: Optional[datetime]
    is_active: bool
    is_unsubscribed: bool
    is_bounced: bool
    source: Optional[str]
    notes: Optional[str]
    tags: list
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LeadList(BaseModel):
    """Schema for list of leads"""
    total: int
    items: list[Lead]