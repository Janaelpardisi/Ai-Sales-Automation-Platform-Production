"""
Analytics API Endpoints
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.campaign import Campaign
from app.models.lead import Lead
from app.models.email import Email

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/campaigns/{campaign_id}/email-stats")
async def get_campaign_email_stats(campaign_id: int):
    """Get email statistics for a campaign"""
    
    async for db in get_db():
        # Get campaign
        result = await db.execute(
            select(Campaign).where(Campaign.id == campaign_id)
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Get leads for this campaign
        result = await db.execute(
            select(Lead).where(Lead.campaign_id == campaign_id)
        )
        leads = result.scalars().all()
        
        # Calculate stats
        total_leads = len(leads)
        total_emails_sent = sum(lead.emails_sent for lead in leads)
        total_emails_opened = sum(lead.emails_opened for lead in leads)
        total_emails_clicked = sum(lead.emails_clicked for lead in leads)
        total_emails_replied = sum(lead.emails_replied for lead in leads)
        
        # Calculate rates
        open_rate = (total_emails_opened / total_emails_sent * 100) if total_emails_sent > 0 else 0
        click_rate = (total_emails_clicked / total_emails_sent * 100) if total_emails_sent > 0 else 0
        reply_rate = (total_emails_replied / total_emails_sent * 100) if total_emails_sent > 0 else 0
        
        # Count unsubscribed
        unsubscribed_count = sum(1 for lead in leads if lead.is_unsubscribed)
        
        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign.name,
            "total_leads": total_leads,
            "emails_sent": total_emails_sent,
            "emails_opened": total_emails_opened,
            "emails_clicked": total_emails_clicked,
            "emails_replied": total_emails_replied,
            "open_rate": round(open_rate, 2),
            "click_rate": round(click_rate, 2),
            "reply_rate": round(reply_rate, 2),
            "unsubscribed_count": unsubscribed_count,
            "engagement_score": round((open_rate + click_rate + reply_rate) / 3, 2)
        }


@router.get("/campaigns/{campaign_id}/leads-stats")
async def get_campaign_leads_stats(campaign_id: int):
    """Get detailed lead statistics for a campaign"""
    
    async for db in get_db():
        # Get campaign
        result = await db.execute(
            select(Campaign).where(Campaign.id == campaign_id)
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Get leads grouped by status
        result = await db.execute(
            select(Lead.status, func.count(Lead.id))
            .where(Lead.campaign_id == campaign_id)
            .group_by(Lead.status)
        )
        status_counts = dict(result.fetchall())
        
        # Get leads grouped by quality
        result = await db.execute(
            select(Lead.quality, func.count(Lead.id))
            .where(Lead.campaign_id == campaign_id)
            .group_by(Lead.quality)
        )
        quality_counts = dict(result.fetchall())
        
        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign.name,
            "leads_by_status": status_counts,
            "leads_by_quality": quality_counts
        }
