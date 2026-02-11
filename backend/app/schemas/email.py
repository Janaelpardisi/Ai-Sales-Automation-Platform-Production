"""
Email Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class EmailBase(BaseModel):
    """Base email schema"""
    to_email: EmailStr
    subject: str = Field(..., min_length=1, max_length=500)
    body_text: str = Field(..., min_length=1)
    body_html: Optional[str] = None


class EmailCreate(EmailBase):
    """Schema for creating an email"""
    lead_id: int
    email_type: str = "initial"
    scheduled_at: Optional[datetime] = None


class EmailUpdate(BaseModel):
    """Schema for updating an email"""
    subject: Optional[str] = None
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class Email(EmailBase):
    """Schema for reading an email"""
    id: int
    lead_id: int
    email_type: str
    from_email: str
    from_name: Optional[str]
    status: str
    is_opened: bool
    is_clicked: bool
    is_replied: bool
    opened_at: Optional[datetime]
    clicked_at: Optional[datetime]
    replied_at: Optional[datetime]
    open_count: int
    click_count: int
    message_id: Optional[str]
    error_message: Optional[str]
    retry_count: int
    personalization_data: dict
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class EmailList(BaseModel):
    """Schema for list of emails"""
    total: int
    items: list[Email]