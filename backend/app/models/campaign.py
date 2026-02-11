"""
Campaign Model
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Campaign(Base):
    """Campaign model"""
    
    __tablename__ = "campaigns"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Basic Information
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Target Criteria
    target_criteria: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Email Configuration
    email_template: Mapped[Optional[str]] = mapped_column(Text)
    subject_template: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Follow-up Configuration
    follow_up_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    follow_up_delays: Mapped[list] = mapped_column(JSON, default=[3, 7, 14])
    max_follow_ups: Mapped[int] = mapped_column(Integer, default=3)
    
    # Personalization
    personalization_level: Mapped[str] = mapped_column(String(20), default="high")
    use_company_research: Mapped[bool] = mapped_column(Boolean, default=True)
    use_news_mentions: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Limits
    daily_limit: Mapped[Optional[int]] = mapped_column(Integer)
    total_limit: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default=CampaignStatus.DRAFT, index=True)
    
    # Statistics
    total_leads: Mapped[int] = mapped_column(Integer, default=0)
    qualified_leads: Mapped[int] = mapped_column(Integer, default=0)
    emails_sent: Mapped[int] = mapped_column(Integer, default=0)
    emails_opened: Mapped[int] = mapped_column(Integer, default=0)
    emails_replied: Mapped[int] = mapped_column(Integer, default=0)
    meetings_booked: Mapped[int] = mapped_column(Integer, default=0)
    
    # Scheduling
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    leads: Mapped[list["Lead"]] = relationship(
        "Lead",
        back_populates="campaign",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Campaign(id={self.id}, name='{self.name}')>"
    
    @property
    def open_rate(self) -> float:
        if self.emails_sent == 0:
            return 0.0
        return self.emails_opened / self.emails_sent
    
    @property
    def reply_rate(self) -> float:
        if self.emails_sent == 0:
            return 0.0
        return self.emails_replied / self.emails_sent
    
    @property
    def conversion_rate(self) -> float:
        if self.qualified_leads == 0:
            return 0.0
        return self.meetings_booked / self.qualified_leads