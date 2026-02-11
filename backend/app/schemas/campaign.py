"""
Campaign Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CampaignBase(BaseModel):
    """Base campaign schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    target_criteria: dict = Field(default_factory=dict)
    email_template: Optional[str] = None
    subject_template: Optional[str] = None
    follow_up_enabled: bool = True
    follow_up_delays: list[int] = [3, 7, 14]
    max_follow_ups: int = Field(default=3, ge=0, le=10)
    personalization_level: str = "high"
    use_company_research: bool = True
    use_news_mentions: bool = True
    daily_limit: Optional[int] = Field(None, ge=1)
    total_limit: Optional[int] = Field(None, ge=1)


class CampaignCreate(CampaignBase):
    """Schema for creating a campaign"""
    pass


class CampaignUpdate(BaseModel):
    """Schema for updating a campaign"""
    name: Optional[str] = None
    description: Optional[str] = None
    target_criteria: Optional[dict] = None
    email_template: Optional[str] = None
    subject_template: Optional[str] = None
    follow_up_enabled: Optional[bool] = None
    follow_up_delays: Optional[list[int]] = None
    max_follow_ups: Optional[int] = None
    personalization_level: Optional[str] = None
    use_company_research: Optional[bool] = None
    use_news_mentions: Optional[bool] = None
    daily_limit: Optional[int] = None
    total_limit: Optional[int] = None
    status: Optional[str] = None


class Campaign(CampaignBase):
    """Schema for reading a campaign"""
    id: int
    status: str
    total_leads: int
    qualified_leads: int
    emails_sent: int
    emails_opened: int
    emails_replied: int
    meetings_booked: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CampaignStats(BaseModel):
    """Campaign statistics"""
    total_leads: int
    qualified_leads: int
    emails_sent: int
    emails_opened: int
    emails_replied: int
    meetings_booked: int
    open_rate: float
    reply_rate: float
    conversion_rate: float


class CampaignList(BaseModel):
    """Schema for list of campaigns"""
    total: int
    items: list[Campaign]