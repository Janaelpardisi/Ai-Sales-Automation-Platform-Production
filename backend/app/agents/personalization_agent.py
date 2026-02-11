"""
Personalization Agent - Creates personalized emails
"""

from typing import Dict, Any
from app.utils.gemini_client import gemini_client


class PersonalizationAgent:
    """Agent for personalizing outreach emails"""
    
    async def generate_email(
        self,
        lead_data: Dict[str, Any],
        template: str = None,
        email_type: str = "initial"
    ) -> Dict[str, str]:
        """Generate personalized email"""
        if not template:
            template = self._get_default_template(email_type)
        
        prompt = f"""
You are an expert B2B sales copywriter. Write a highly personalized cold email.

LEAD INFORMATION:
- Company: {lead_data.get('company_name', 'the company')}
- Industry: {lead_data.get('industry', 'your industry')}
- Contact Name: {lead_data.get('contact_name', 'there')}
- Contact Title: {lead_data.get('contact_title', '')}
- Company Size: {lead_data.get('company_size', '')}
- Pain Points: {lead_data.get('pain_points', [])}
- Recent News: {lead_data.get('recent_news', 'None')}

EMAIL TYPE: {email_type}

TEMPLATE/GUIDELINES:
{template}

REQUIREMENTS:
1. Subject line: Compelling, personalized, under 50 characters
2. Body: 
   - Short (100-150 words max)
   - Personalized with specific company details
   - Address a specific pain point
   - Clear value proposition
   - Single, clear call-to-action
   - Professional but conversational tone
3. NO generic templates or obvious sales language
4. Reference specific details about their company

Return as JSON:
{{
    "subject": "subject line here",
    "body": "email body here"
}}
"""
        
        try:
            result = await gemini_client.generate_json(prompt)
            return {
                "subject": result.get("subject", "Quick question"),
                "body": result.get("body", ""),
            }
        except Exception as e:
            return self._create_fallback_email(lead_data)
    
    async def generate_follow_up(
        self,
        lead_data: Dict[str, Any],
        previous_email: str,
        follow_up_number: int
    ) -> Dict[str, str]:
        """Generate follow-up email"""
        prompt = f"""
Write a follow-up email (Follow-up #{follow_up_number}).

PREVIOUS EMAIL:
{previous_email}

LEAD INFO:
- Company: {lead_data.get('company_name', 'the company')}
- Name: {lead_data.get('contact_name', 'there')}

REQUIREMENTS:
- Keep it SHORT (50-75 words)
- Different angle than previous email
- Add value, not just "checking in"
- Soft CTA
- Maintain thread context

Return JSON:
{{
    "subject": "Re: [previous subject] or new angle",
    "body": "follow-up body"
}}
"""
        
        try:
            result = await gemini_client.generate_json(prompt)
            return {
                "subject": result.get("subject", f"Re: Following up"),
                "body": result.get("body", ""),
            }
        except:
            return self._create_fallback_follow_up(lead_data, follow_up_number)
    
    def _get_default_template(self, email_type: str) -> str:
        """Get default template for email type"""
        templates = {
            "initial": """
Write a cold email that:
- Opens with a personalized observation about their company
- Mentions a specific pain point relevant to their industry
- Offers clear value (not a generic pitch)
- Ends with a simple question or soft CTA
            """,
            "follow_up_1": """
First follow-up:
- Reference the previous email briefly
- Share a new insight or resource
- Make it easy to respond with a yes/no question
            """,
        }
        return templates.get(email_type, templates["initial"])
    
    def _create_fallback_email(self, lead_data: Dict[str, Any]) -> Dict[str, str]:
        """Create basic fallback email if AI generation fails"""
        company = lead_data.get("company_name", "your company")
        name = lead_data.get("contact_name", "there")
        
        return {
            "subject": f"Quick question about {company}",
            "body": f"""Hi {name},

I noticed {company} and wanted to reach out.

Would you be open to a brief conversation?

Best regards"""
        }
    
    def _create_fallback_follow_up(self, lead_data: Dict[str, Any], follow_up_number: int) -> Dict[str, str]:
        """Create basic fallback follow-up"""
        name = lead_data.get("contact_name", "there")
        
        return {
            "subject": "Following up",
            "body": f"""Hi {name},

Just wanted to follow up on my previous email.

Would love to hear your thoughts.

Best"""
        }


# Global instance
personalization_agent = PersonalizationAgent()