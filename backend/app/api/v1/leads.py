"""
Leads API Routes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.lead import Lead, LeadCreate, LeadUpdate, LeadList
from app.services.lead_service import lead_service

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("/", response_model=Lead, status_code=201)
async def create_lead(
    lead_data: LeadCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new lead"""
    lead = await lead_service.create_lead(db, lead_data)
    return lead


@router.get("/{lead_id}", response_model=Lead)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific lead by ID"""
    lead = await lead_service.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.get("/", response_model=LeadList)
async def list_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    campaign_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List leads with optional filters"""
    leads = await lead_service.get_leads(
        db,
        skip=skip,
        limit=limit,
        campaign_id=campaign_id,
        status=status
    )
    total = await lead_service.count_leads(
        db,
        campaign_id=campaign_id,
        status=status
    )
    
    return LeadList(total=total, items=leads)


@router.put("/{lead_id}", response_model=Lead)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a lead"""
    lead = await lead_service.update_lead(db, lead_id, lead_update)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.delete("/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a lead"""
    success = await lead_service.delete_lead(db, lead_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lead not found")
    return None