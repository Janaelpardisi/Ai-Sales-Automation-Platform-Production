"""
Lead Service - Business logic for leads
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lead import Lead, LeadStatus
from app.schemas.lead import LeadCreate, LeadUpdate


class LeadService:
    """Service for managing leads"""
    
    async def create_lead(self, db: AsyncSession, lead_data: LeadCreate) -> Lead:
        """Create a new lead"""
        lead = Lead(**lead_data.model_dump())
        db.add(lead)
        await db.commit()
        await db.refresh(lead)
        return lead
    
    async def get_lead(self, db: AsyncSession, lead_id: int) -> Optional[Lead]:
        """Get lead by ID"""
        result = await db.execute(select(Lead).where(Lead.id == lead_id))
        return result.scalar_one_or_none()
    
    async def get_leads(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        campaign_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Lead]:
        """Get list of leads with filters"""
        query = select(Lead)
        
        if campaign_id:
            query = query.where(Lead.campaign_id == campaign_id)
        if status:
            query = query.where(Lead.status == status)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def update_lead(
        self,
        db: AsyncSession,
        lead_id: int,
        lead_update: LeadUpdate
    ) -> Optional[Lead]:
        """Update a lead"""
        lead = await self.get_lead(db, lead_id)
        if not lead:
            return None
        
        update_data = lead_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lead, field, value)
        
        await db.commit()
        await db.refresh(lead)
        return lead
    
    async def delete_lead(self, db: AsyncSession, lead_id: int) -> bool:
        """Delete a lead"""
        lead = await self.get_lead(db, lead_id)
        if not lead:
            return False
        
        await db.delete(lead)
        await db.commit()
        return True
    
    async def count_leads(
        self,
        db: AsyncSession,
        campaign_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> int:
        """Count leads with filters"""
        from sqlalchemy import func
        
        query = select(func.count(Lead.id))
        
        if campaign_id:
            query = query.where(Lead.campaign_id == campaign_id)
        if status:
            query = query.where(Lead.status == status)
        
        result = await db.execute(query)
        return result.scalar() or 0


# Global instance
lead_service = LeadService()