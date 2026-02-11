"""
Lead Model
"""

from datetime import datetime
from enum import Enum
from typing import Optional
import secrets
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class LeadStatus(str, Enum):
    NEW = "new"
    RESEARCHING = "researching"
    QUALIFIED = "qualified"
    DISQUALIFIED = "disqualified"
    CONTACTED = "contacted"
    RESPONDED = "responded"
    MEETING_BOOKED = "meeting_booked"
    WON = "won"
    LOST = "lost"


class LeadQuality(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


class Lead(Base):
    """Lead model"""
    
    __tablename__ = "leads"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Campaign relationship
    campaign_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    # Company Information
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    company_website: Mapped[Optional[str]] = mapped_column(String(500))
    company_domain: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    company_linkedin: Mapped[Optional[str]] = mapped_column(String(500))
    
    industry: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    company_size: Mapped[Optional[str]] = mapped_column(String(50))
    location: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Contact Information
    contact_name: Mapped[Optional[str]] = mapped_column(String(255))
    contact_title: Mapped[Optional[str]] = mapped_column(String(255))
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50))
    contact_linkedin: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Lead Scoring
    quality_score: Mapped[Optional[float]] = mapped_column(Float)
    quality: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Status
    status: Mapped[str] = mapped_column(String(50), default=LeadStatus.NEW, index=True)
    
    # Enrichment Data
    enrichment_data: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)
    
    # Engagement Tracking
    emails_sent: Mapped[int] = mapped_column(Integer, default=0)
    emails_opened: Mapped[int] = mapped_column(Integer, default=0)
    emails_clicked: Mapped[int] = mapped_column(Integer, default=0)
    emails_replied: Mapped[int] = mapped_column(Integer, default=0)
    
    last_contacted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    next_follow_up_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Flags
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_unsubscribed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bounced: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Unsubscribe token for secure unsubscribe links
    unsubscribe_token: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    
    # Metadata
    source: Mapped[Optional[str]] = mapped_column(String(100))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    tags: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    campaign: Mapped[Optional["Campaign"]] = relationship("Campaign", back_populates="leads")
    emails: Mapped[list["Email"]] = relationship(
        "Email",
        back_populates="lead",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Lead(id={self.id}, company='{self.company_name}')>"
    
    @property
    def engagement_score(self) -> float:
        if self.emails_sent == 0:
            return 0.0
        open_rate = self.emails_opened / self.emails_sent
        click_rate = self.emails_clicked / self.emails_sent if self.emails_sent > 0 else 0
        reply_rate = self.emails_replied / self.emails_sent if self.emails_sent > 0 else 0
        return (open_rate * 0.3) + (click_rate * 0.3) + (reply_rate * 0.4)
    
    def generate_unsubscribe_token(self) -> str:
        """Generate a secure unsubscribe token"""
        if not self.unsubscribe_token:
            self.unsubscribe_token = secrets.token_urlsafe(32)
        return self.unsubscribe_token