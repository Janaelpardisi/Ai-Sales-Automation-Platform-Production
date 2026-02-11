"""
Campaigns API Routes
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.campaign import (
    Campaign,
    CampaignCreate,
    CampaignUpdate,
    CampaignList,
    CampaignStats
)
from app.services.campaign_service import campaign_service

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("/", response_model=Campaign, status_code=201)
async def create_campaign(
    campaign_data: CampaignCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new campaign"""
    campaign = await campaign_service.create_campaign(db, campaign_data)
    return campaign


@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific campaign by ID"""
    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.get("/", response_model=CampaignList)
async def list_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List campaigns with optional filters"""
    campaigns = await campaign_service.get_campaigns(
        db,
        skip=skip,
        limit=limit,
        status=status
    )
    
    # Simple count (could be optimized)
    total = len(campaigns)
    
    return CampaignList(total=total, items=campaigns)


@router.put("/{campaign_id}", response_model=Campaign)
async def update_campaign(
    campaign_id: int,
    campaign_update: CampaignUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a campaign"""
    campaign = await campaign_service.update_campaign(db, campaign_id, campaign_update)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.delete("/{campaign_id}", status_code=204)
async def delete_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a campaign"""
    success = await campaign_service.delete_campaign(db, campaign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return None


@router.post("/{campaign_id}/run")
async def run_campaign(
    campaign_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Execute campaign workflow"""
    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Run campaign in background
    try:
        result = await campaign_service.run_campaign(db, campaign_id)
        return {
            "status": "success",
            "message": "Campaign executed successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}/stats", response_model=CampaignStats)
async def get_campaign_stats(
    campaign_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get campaign statistics"""
    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return CampaignStats(
        total_leads=campaign.total_leads,
        qualified_leads=campaign.qualified_leads,
        emails_sent=campaign.emails_sent,
        emails_opened=campaign.emails_opened,
        emails_replied=campaign.emails_replied,
        meetings_booked=campaign.meetings_booked,
        open_rate=campaign.open_rate,
        reply_rate=campaign.reply_rate,
        conversion_rate=campaign.conversion_rate,
    )