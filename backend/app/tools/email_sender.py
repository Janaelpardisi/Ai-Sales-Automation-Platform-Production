"""
Email Sender Tool
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import aiosmtplib
from app.config import settings


class EmailSender:
    """Send emails via SMTP"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.from_name = settings.SMTP_FROM_NAME
        self.base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> bool:
        """Send email via SMTP"""
        if not self.smtp_user or not self.smtp_password:
            raise Exception("SMTP credentials not configured")
        
        from_email = from_email or self.from_email
        from_name = from_name or self.from_name
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = f"{from_name} <{from_email}>"
        message['To'] = to_email
        
        # Add plain text part
        part1 = MIMEText(body_text, 'plain')
        message.attach(part1)
        
        # Add HTML part if provided
        if body_html:
            part2 = MIMEText(body_html, 'html')
            message.attach(part2)
        
        try:
            # Send using aiosmtplib (async)
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True,  # Use STARTTLS for Outlook
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
    
    def create_unsubscribe_link(self, unsubscribe_token: str) -> str:
        """Generate unsubscribe link using secure token"""
        return f"{self.base_url}/api/v1/unsubscribe/{unsubscribe_token}"
    
    async def send_to_lead(
        self,
        lead,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
    ) -> bool:
        """
        Send email to a lead with automatic unsubscribe link
        
        Args:
            lead: Lead model instance (must have contact_email and unsubscribe_token)
            subject: Email subject
            body_text: Plain text body
            body_html: HTML body (optional)
        
        Returns:
            bool: True if sent successfully
        
        Raises:
            Exception: If lead is unsubscribed or email sending fails
        """
        # Check if lead is unsubscribed
        if lead.is_unsubscribed:
            raise Exception(f"Lead {lead.id} ({lead.company_name}) is unsubscribed")
        
        # Check if lead has email
        if not lead.contact_email:
            raise Exception(f"Lead {lead.id} ({lead.company_name}) has no email address")
        
        # Generate unsubscribe token if not exists
        if not lead.unsubscribe_token:
            lead.generate_unsubscribe_token()
        
        # Create unsubscribe link
        unsubscribe_link = self.create_unsubscribe_link(lead.unsubscribe_token)
        
        # Add unsubscribe link to body_text if not already present
        if '{unsubscribe_link}' not in body_text:
            body_text += f"\n\n---\nTo unsubscribe, click here: {unsubscribe_link}"
        
        # Replace placeholder in body_html if present
        if body_html and '{unsubscribe_link}' in body_html:
            body_html = body_html.replace('{unsubscribe_link}', unsubscribe_link)
        
        # Send email
        return await self.send_email(
            to_email=lead.contact_email,
            subject=subject,
            body_text=body_text,
            body_html=body_html
        )


# Global instance
email_sender = EmailSender()
