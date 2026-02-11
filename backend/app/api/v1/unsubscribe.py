"""
Unsubscribe API Endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.lead import Lead
from app.core.logging import logger

router = APIRouter(prefix="/unsubscribe", tags=["unsubscribe"])


@router.get("/{token}", response_class=HTMLResponse)
async def unsubscribe_page(token: str, request: Request):
    """Unsubscribe page - shows confirmation and processes unsubscribe"""
    
    # Get database session
    async for db in get_db():
        # Find lead by token
        result = await db.execute(
            select(Lead).where(Lead.unsubscribe_token == token)
        )
        lead = result.scalar_one_or_none()
        
        if not lead:
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Invalid Link</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
                    .error { color: #d32f2f; }
                </style>
            </head>
            <body>
                <h1 class="error">Invalid Unsubscribe Link</h1>
                <p>This unsubscribe link is invalid or has expired.</p>
            </body>
            </html>
            """
        
        # Check if already unsubscribed
        if lead.is_unsubscribed:
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Already Unsubscribed</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
                    .success {{ color: #388e3c; }}
                </style>
            </head>
            <body>
                <h1 class="success">Already Unsubscribed</h1>
                <p>You have already unsubscribed from our emails.</p>
                <p>Company: <strong>{lead.company_name}</strong></p>
            </body>
            </html>
            """
        
        # Process unsubscribe
        lead.is_unsubscribed = True
        await db.commit()
        
        logger.info(f"Lead {lead.id} ({lead.company_name}) unsubscribed via token")
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Successfully Unsubscribed</title>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #388e3c;
                    margin-top: 0;
                }}
                .icon {{
                    font-size: 48px;
                    margin-bottom: 20px;
                }}
                .company {{
                    background: #f5f5f5;
                    padding: 10px;
                    border-radius: 4px;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #666;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">✅</div>
                <h1>Successfully Unsubscribed</h1>
                <p>You have been successfully unsubscribed from our email list.</p>
                
                <div class="company">
                    <strong>Company:</strong> {lead.company_name}
                </div>
                
                <p>You will no longer receive emails from us.</p>
                
                <div class="footer">
                    <p>If you unsubscribed by mistake, please contact us directly.</p>
                </div>
            </div>
        </body>
        </html>
        """


@router.get("/status/{token}")
async def check_unsubscribe_status(token: str):
    """Check if a lead is unsubscribed (API endpoint)"""
    
    async for db in get_db():
        result = await db.execute(
            select(Lead).where(Lead.unsubscribe_token == token)
        )
        lead = result.scalar_one_or_none()
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        return {
            "company_name": lead.company_name,
            "is_unsubscribed": lead.is_unsubscribed,
            "unsubscribed_at": lead.updated_at if lead.is_unsubscribed else None
        }
