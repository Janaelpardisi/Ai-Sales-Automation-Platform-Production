"""
Campaign Service - Business logic for campaigns
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.campaign import Campaign, CampaignStatus
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.agents.orchestrator import orchestrator_agent
from app.services.lead_service import lead_service
from app.schemas.lead import LeadCreate
from app.tools.email_finder import email_finder
from app.tools.email_sender import email_sender
from app.utils.email_templates import render_template, get_default_variables
from app.core.logging import logger
from app.config import settings


class CampaignService:
    """Service for managing campaigns"""
    
    async def create_campaign(self, db: AsyncSession, campaign_data: CampaignCreate) -> Campaign:
        """Create a new campaign"""
        campaign = Campaign(**campaign_data.model_dump())
        db.add(campaign)
        await db.commit()
        await db.refresh(campaign)
        return campaign
    
    async def get_campaign(self, db: AsyncSession, campaign_id: int) -> Optional[Campaign]:
        """Get campaign by ID"""
        result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
        return result.scalar_one_or_none()
    
    async def get_campaigns(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Campaign]:
        """Get list of campaigns"""
        query = select(Campaign)
        
        if status:
            query = query.where(Campaign.status == status)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def update_campaign(
        self,
        db: AsyncSession,
        campaign_id: int,
        campaign_update: CampaignUpdate
    ) -> Optional[Campaign]:
        """Update a campaign"""
        campaign = await self.get_campaign(db, campaign_id)
        if not campaign:
            return None
        
        update_data = campaign_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(campaign, field, value)
        
        await db.commit()
        await db.refresh(campaign)
        return campaign
    
    async def delete_campaign(self, db: AsyncSession, campaign_id: int) -> bool:
        """Delete a campaign"""
        campaign = await self.get_campaign(db, campaign_id)
        if not campaign:
            return False
        
        await db.delete(campaign)
        await db.commit()
        return True
    
    async def run_campaign(self, db: AsyncSession, campaign_id: int) -> dict:
        """Execute campaign workflow"""
        logger.info(f"🚀 Starting campaign {campaign_id}...")
        
        campaign = await self.get_campaign(db, campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        
        logger.info(f"✅ Campaign found: {campaign.name}")
        
        # Prepare campaign criteria
        target_criteria = campaign.target_criteria or {}
        criteria = {
            "industry": target_criteria.get("industry", ""),
            "location": target_criteria.get("location", ""),
            "company_size": target_criteria.get("company_size", ""),
            "email_template": campaign.email_template,
        }
        
        logger.info(f"📋 Campaign criteria: {criteria}")
        
        # Use real search if enabled, otherwise mock data
        from app.config import settings
        
        if settings.USE_REAL_SEARCH:
            logger.info("🔍 Using REAL data via SerpAPI...")
            
            # Use SerpAPI directly (bypass LangGraph completely)
            try:
                from app.tools.web_scraper import web_scraper
                from app.agents.qualification_agent import qualification_agent
                from app.utils.gemini_client import gemini_client
                
                # Step 1: Generate search queries using Gemini
                logger.info("🤖 Generating search queries...")
                query_prompt = f"""
Generate 3 specific search queries to find companies matching these criteria:
- Industry: {criteria.get('industry', 'any')}
- Location: {criteria.get('location', 'any')}
- Company Size: {criteria.get('company_size', 'any')}

Return as JSON array of strings.
Example: ["SaaS companies in USA", "cloud software providers United States"]
"""
                search_queries = await gemini_client.generate_json(query_prompt)
                if not search_queries or not isinstance(search_queries, list):
                    search_queries = [f"{criteria.get('industry', 'technology')} companies in {criteria.get('location', 'USA')}"]
                
                logger.info(f"📝 Generated {len(search_queries)} search queries")
                
                # Step 2: Search using SerpAPI
                logger.info("📡 Searching Google via SerpAPI...")
                all_results = []
                for query in search_queries[:3]:
                    try:
                        results = await web_scraper.google_search_real(query, num_results=5)
                        all_results.extend(results)
                    except Exception as e:
                        logger.warning(f"⚠️  Search failed for '{query}': {str(e)}")
                        continue
                
                logger.info(f"✅ Found {len(all_results)} companies from Google")
                
                # Step 3: Convert to lead format
                leads = []
                for result in all_results:
                    lead = {
                        "company_name": result.get("title", "Unknown Company"),
                        "website": result.get("url", ""),
                        "domain": result.get("url", "").replace("https://", "").replace("http://", "").split("/")[0],
                        "industry": criteria.get("industry", "Technology"),
                        "location": criteria.get("location", "USA"),
                        "source": "google_search_real",
                        "description": result.get("snippet", "")
                    }
                    leads.append(lead)
                
                # Step 4: Qualify leads and find emails
                from app.tools.email_finder import email_finder
                
                qualified_leads = []
                for lead in leads:
                    try:
                        score_result = await qualification_agent.score_lead(lead, criteria)
                        lead["quality_score"] = score_result["score"]
                        lead["quality"] = score_result["quality"]
                        lead["qualification_reasoning"] = score_result["reasoning"]
                        
                        # Find contact email (Hunter.io if enabled, otherwise fallback)
                        contact_email = await email_finder.find_contact_email(
                            company_domain=lead.get("domain"),
                            company_website=lead.get("website"),
                            company_name=lead.get("company_name")
                        )
                        
                        lead["contact_email"] = contact_email or "ganaaliahmed00@gmail.com"  # Fallback
                        
                        if qualification_agent.is_qualified(score_result["score"]):
                            qualified_leads.append(lead)
                    except Exception as e:
                        logger.warning(f"⚠️  Failed to qualify {lead.get('company_name')}: {str(e)}")
                        continue
                
                logger.info(f"✅ Qualified {len(qualified_leads)} leads out of {len(leads)} total")
                
            except Exception as e:
                logger.error(f"❌ Real search failed: {str(e)}")
                import traceback
                traceback.print_exc()
                logger.info("⚠️  Falling back to mock data...")
                qualified_leads = await self._generate_mock_leads(target_criteria)
        else:
            logger.info("🎲 Using MOCK data for testing...")
            qualified_leads = await self._generate_mock_leads(target_criteria)
        
        logger.info(f"✅ Total qualified leads: {len(qualified_leads)}")
        
        # Validate results
        if not qualified_leads:
            return {
                "campaign_id": campaign_id,
                "leads_found": 0,
                "leads_created": 0,
                "message": "No leads found matching the criteria"
            }
        
        # Save leads to database
        created_leads = []
        logger.info(f"📝 Creating {len(qualified_leads)} leads in database...")
        
        for lead_data in qualified_leads:
            # Skip None or invalid lead data
            if not lead_data or not isinstance(lead_data, dict):
                logger.warning(f"⚠️  Skipping invalid lead data: {lead_data}")
                continue
                
            try:
                lead_create = LeadCreate(
                    campaign_id=campaign_id,
                    company_name=lead_data.get("company_name", "Unknown"),
                    company_website=lead_data.get("website"),
                    company_domain=lead_data.get("domain"),
                    industry=lead_data.get("industry"),
                    location=lead_data.get("location"),
                    description=lead_data.get("description"),
                    source=lead_data.get("source"),
                )
                lead = await lead_service.create_lead(db, lead_create)
                logger.info(f"✅ Created lead: {lead.company_name} (ID={lead.id})")
                
                # Update with qualification data
                from app.schemas.lead import LeadUpdate
                lead_update = LeadUpdate(
                    quality_score=lead_data.get("quality_score"),
                    quality=lead_data.get("quality"),
                    notes=lead_data.get("qualification_reasoning"),
                )
                lead = await lead_service.update_lead(db, lead.id, lead_update)
                created_leads.append(lead)
            except Exception as e:
                logger.error(f"❌ Failed to create lead {lead_data.get('company_name')}: {str(e)}")
                continue
        
        logger.info(f"✅ Created {len(created_leads)} leads successfully")
        
        # Update campaign statistics
        campaign.total_leads = len(qualified_leads)
        campaign.qualified_leads = len(qualified_leads)
        campaign.status = CampaignStatus.ACTIVE
        await db.commit()
        
        # Send emails to leads
        emails_sent = 0
        emails_failed = 0
        
        for lead in created_leads:
            try:
                # Find contact email if not exists
                if not lead.contact_email:
                    contact_email = await email_finder.find_contact_email(
                        company_domain=lead.company_domain,
                        company_website=lead.company_website,
                        contact_name=lead.contact_name
                    )
                    
                    if contact_email:
                        lead.contact_email = contact_email
                        await db.commit()
                    else:
                        logger.warning(f"Could not find email for lead {lead.id} ({lead.company_name})")
                        continue
                
                # Generate unsubscribe token
                if not lead.unsubscribe_token:
                    lead.generate_unsubscribe_token()
                    await db.commit()
                
                # Prepare template variables
                variables = get_default_variables(
                    company_name=lead.company_name,
                    contact_name=lead.contact_name or "there",
                    industry=lead.industry or "your industry",
                    product="our AI-powered solution",
                    value_proposition="automate lead generation and save valuable time",
                    sender_name=settings.SMTP_FROM_NAME or "Sales Team",
                    sender_title="Business Development",
                    unsubscribe_link=email_sender.create_unsubscribe_link(lead.unsubscribe_token)
                )
                
                # Render email template
                rendered = render_template('initial', **variables)
                
                # Send email
                await email_sender.send_to_lead(
                    lead=lead,
                    subject=rendered['subject'],
                    body_text=rendered['body_text'],
                    body_html=rendered['body_html']
                )
                
                # Update lead stats
                lead.emails_sent += 1
                lead.last_contacted_at = datetime.utcnow()
                lead.status = "contacted"
                await db.commit()
                
                emails_sent += 1
                logger.info(f"✅ Email sent to {lead.company_name} ({lead.contact_email})")
                
            except Exception as e:
                emails_failed += 1
                logger.error(f"❌ Failed to send email to {lead.company_name}: {str(e)}")
                continue
        
        # Update campaign email stats
        campaign.emails_sent = emails_sent
        await db.commit()
        
        return {
            "campaign_id": campaign_id,
            "leads_found": len(qualified_leads),
            "leads_created": len(created_leads),
            "emails_sent": emails_sent,
            "emails_failed": emails_failed
        }
    
    async def _generate_mock_leads(self, target_criteria: dict) -> list:
        """Generate mock leads for testing (fallback when real search is disabled)"""
        import random
        
        industries = ["Technology", "SaaS", "FinTech", "E-commerce", "Healthcare"]
        locations = ["Egypt", "UAE", "Saudi Arabia", "USA", "UK"]
        companies = [
            "TechCorp Solutions", "Digital Innovations Ltd", "Smart Systems Inc",
            "Future Tech Co", "AI Dynamics", "CloudBase Systems", "DataFlow Solutions",
            "NextGen Software", "Quantum Analytics", "Cyber Solutions Group"
        ]
        
        qualified_leads = []
        num_leads = random.randint(3, 8)
        
        for i in range(num_leads):
            company = random.choice(companies)
            campaign_location = target_criteria.get("location", "").strip()
            lead_location = campaign_location if campaign_location else random.choice(locations)
            
            campaign_industry = target_criteria.get("industry", "").strip()
            lead_industry = campaign_industry if campaign_industry else random.choice(industries)
            
            lead = {
                "company_name": company + f" {i+1}",
                "website": f"https://example-company-{i+1}.com",
                "domain": f"company{i+1}.com",
                "contact_name": f"John Doe {i+1}",
                "contact_email": "ganaaliahmed00@gmail.com",
                "industry": lead_industry,
                "location": lead_location,
                "source": "mock_data",
                "description": f"A leading company in {lead_industry} sector",
                "quality_score": round(random.uniform(0.6, 0.95), 2),
                "quality": random.choice(["hot", "warm", "warm", "hot"]),
                "qualification_reasoning": "Strong fit based on industry and company size criteria"
            }
            qualified_leads.append(lead)
        
        return qualified_leads


# Global instance
campaign_service = CampaignService()