"""
Email Finder Tool
"""

import re
from typing import Optional, List
import httpx
from email_validator import validate_email, EmailNotValidError


class EmailFinder:
    """Find and validate email addresses"""
    
    COMMON_PATTERNS = [
        "{first}.{last}@{domain}",
        "{first}@{domain}",
        "{f}{last}@{domain}",
        "{first}{last}@{domain}",
        "{first}_{last}@{domain}",
    ]
    
    async def find_email_hunter(self, domain: str, company_name: Optional[str] = None) -> Optional[str]:
        """
        Find email using Hunter.io API
        
        Args:
            domain: Company domain (e.g., 'example.com')
            company_name: Optional company name for better results
        
        Returns:
            Email address or None
        """
        from app.config import settings
        
        if not settings.HUNTER_API_KEY:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                # Domain Search API - finds emails from a domain
                url = "https://api.hunter.io/v2/domain-search"
                params = {
                    "domain": domain,
                    "api_key": settings.HUNTER_API_KEY,
                    "limit": 5  # Get top 5 emails
                }
                
                if company_name:
                    params["company"] = company_name
                
                response = await client.get(url, params=params, timeout=15.0)
                
                if response.status_code == 200:
                    data = response.json()
                    emails = data.get("data", {}).get("emails", [])
                    
                    if emails:
                        # Prefer generic emails (info@, contact@, etc.)
                        for email_data in emails:
                            email = email_data.get("value")
                            email_type = email_data.get("type", "")
                            
                            if email_type == "generic" and email:
                                return email
                        
                        # Otherwise return first email
                        first_email = emails[0].get("value")
                        if first_email:
                            return first_email
                
                return None
                
        except Exception as e:
            print(f"⚠️ Hunter.io API error: {str(e)}")
            return None
    
    async def find_email_snov(self, domain: str, company_name: Optional[str] = None) -> Optional[str]:
        """
        Find email using Snov.io API
        
        Args:
            domain: Company domain (e.g., 'example.com')
            company_name: Optional company name
        
        Returns:
            Email address or None
        """
        from app.config import settings
        
        if not settings.SNOV_API_KEY:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                # Domain Search API
                url = "https://api.snov.io/v1/get-domain-emails-with-info"
                headers = {
                    "Authorization": f"Bearer {settings.SNOV_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "domain": domain,
                    "type": "all",
                    "limit": 10
                }
                
                response = await client.post(url, headers=headers, json=data, timeout=15.0)
                
                if response.status_code == 200:
                    result = response.json()
                    emails = result.get("emails", [])
                    
                    if emails:
                        # Prefer generic/company emails
                        for email_data in emails:
                            email = email_data.get("email")
                            email_type = email_data.get("type", "")
                            
                            if email and email_type in ["generic", "company"]:
                                return email
                        
                        # Otherwise return first valid email
                        first_email = emails[0].get("email")
                        if first_email:
                            return first_email
                
                return None
                
        except Exception as e:
            print(f"⚠️ Snov.io API error: {str(e)}")
            return None
    
    async def find_email_apollo(self, domain: str, company_name: Optional[str] = None) -> Optional[str]:
        """
        Find email using Apollo.io API
        
        Args:
            domain: Company domain (e.g., 'example.com')
            company_name: Optional company name
        
        Returns:
            Email address or None
        """
        from app.config import settings
        
        if not settings.APOLLO_API_KEY:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                # People Search & Enrichment API
                url = "https://api.apollo.io/v1/mixed_people/search"
                headers = {
                    "Content-Type": "application/json",
                    "Cache-Control": "no-cache"
                }
                data = {
                    "api_key": settings.APOLLO_API_KEY,
                    "q_organization_domains": domain,
                    "page": 1,
                    "per_page": 10
                }
                
                response = await client.post(url, headers=headers, json=data, timeout=15.0)
                
                if response.status_code == 200:
                    result = response.json()
                    people = result.get("people", [])
                    
                    if people:
                        # Prefer people with verified emails
                        for person in people:
                            email = person.get("email")
                            email_status = person.get("email_status", "")
                            
                            if email and email_status == "verified":
                                return email
                        
                        # Otherwise return first available email
                        first_person = people[0]
                        email = first_person.get("email")
                        if email:
                            return email
                
                return None
                
        except Exception as e:
            print(f"⚠️ Apollo.io API error: {str(e)}")
            return None
    
    def generate_email_patterns(
        self,
        first_name: str,
        last_name: str,
        domain: str
    ) -> List[str]:
        """Generate possible email patterns"""
        first = first_name.lower().strip()
        last = last_name.lower().strip()
        f = first[0] if first else ""
        
        emails = []
        for pattern in self.COMMON_PATTERNS:
            email = pattern.format(
                first=first,
                last=last,
                f=f,
                domain=domain
            )
            emails.append(email)
        
        return emails
    
    def validate_email_format(self, email: str) -> bool:
        """Validate email format"""
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False
    
    async def verify_email_smtp(self, email: str) -> bool:
        """
        Verify email via SMTP (simplified)
        
        For production use:
        - EmailHippo: https://www.emailhippo.com/
        - NeverBounce: https://neverbounce.com/
        - ZeroBounce: https://www.zerobounce.net/
        """
        # Basic format validation for now
        return self.validate_email_format(email)
    
    async def find_email_from_website(self, url: str) -> List[str]:
        """Extract emails from website"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0, follow_redirects=True)
                text = response.text
            
            # Simple regex to find emails
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, text)
            
            # Validate and deduplicate
            valid_emails = []
            seen = set()
            for email in emails:
                if self.validate_email_format(email) and email not in seen:
                    valid_emails.append(email)
                    seen.add(email)
            
            return valid_emails
        except Exception:
            return []
    
    def extract_domain_from_url(self, url: str) -> str:
        """Extract domain from URL"""
        domain = url.replace('https://', '').replace('http://', '')
        domain = domain.replace('www.', '')
        domain = domain.split('/')[0]
        return domain
    
    async def find_contact_email(
        self,
        company_domain: Optional[str] = None,
        company_website: Optional[str] = None,
        contact_name: Optional[str] = None,
        company_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Find contact email using various strategies
        
        Args:
            company_domain: Company domain (e.g., 'example.com')
            company_website: Company website URL
            contact_name: Contact name (e.g., 'John Doe')
            company_name: Company name for Hunter.io search
        
        Returns:
            Email address or None
        """
        from app.config import settings
        
        # Extract domain from website if not provided
        if not company_domain and company_website:
            company_domain = self.extract_domain_from_url(company_website)
        
        if not company_domain:
            return None
        
        # Strategy 1: Email APIs (Apollo.io, Snov.io, or Hunter.io)
        if settings.USE_REAL_EMAILS:
            # Try Apollo.io first (unlimited searches!)
            if settings.APOLLO_API_KEY:
                email = await self.find_email_apollo(company_domain, company_name)
                if email:
                    print(f"✅ Found email via Apollo.io: {email}")
                    return email
            
            # Try Snov.io second (50 credits/month)
            if settings.SNOV_API_KEY:
                email = await self.find_email_snov(company_domain, company_name)
                if email:
                    print(f"✅ Found email via Snov.io: {email}")
                    return email
            
            # Try Hunter.io as last resort (25 credits/month)
            if settings.HUNTER_API_KEY:
                email = await self.find_email_hunter(company_domain, company_name)
                if email:
                    print(f"✅ Found email via Hunter.io: {email}")
                    return email
        
        # Strategy 2: Try to find email from website
        if company_website:
            emails = await self.find_email_from_website(company_website)
            if emails:
                # Prefer emails from the same domain
                for email in emails:
                    if company_domain in email:
                        return email
                # Otherwise return first valid email
                return emails[0]
        
        # Strategy 3: Generate patterns if we have contact name
        if contact_name:
            # Parse name
            name_parts = contact_name.strip().split()
            if len(name_parts) >= 2:
                first_name = name_parts[0]
                last_name = name_parts[-1]
                
                # Generate possible emails
                patterns = self.generate_email_patterns(first_name, last_name, company_domain)
                
                # Return first valid pattern (basic validation only)
                for email in patterns:
                    if self.validate_email_format(email):
                        return email
        
        # Strategy 4: Try common patterns
        common_emails = [
            f"info@{company_domain}",
            f"contact@{company_domain}",
            f"hello@{company_domain}",
            f"sales@{company_domain}"
        ]
        
        for email in common_emails:
            if self.validate_email_format(email):
                return email
        
        return None


# Global instance
email_finder = EmailFinder()