"""
Email Templates - Simple template system using Python string formatting
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class EmailTemplate:
    """Email template with subject and body"""
    name: str
    subject: str
    body_text: str
    body_html: str
    
    def render(self, **kwargs) -> Dict[str, str]:
        """Render template with provided variables"""
        return {
            'subject': self.subject.format(**kwargs),
            'body_text': self.body_text.format(**kwargs),
            'body_html': self.body_html.format(**kwargs)
        }


# Default Templates
INITIAL_OUTREACH = EmailTemplate(
    name="initial_outreach",
    subject="Quick question about {company}",
    body_text="""Hi {name},

I noticed {company} is doing great work in the {industry} space. I wanted to reach out because I think {product} could help you {value_proposition}.

Would you be open to a quick 15-minute call to explore how we might be able to help?

Best regards,
{sender_name}
{sender_title}

---
If you'd prefer not to receive these emails, you can unsubscribe here: {unsubscribe_link}""",
    
    body_html="""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ margin-bottom: 20px; }}
        .content {{ margin-bottom: 30px; }}
        .signature {{ margin-top: 30px; color: #666; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #999; }}
        .unsubscribe {{ color: #666; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <p>Hi {name},</p>
            
            <p>I noticed <strong>{company}</strong> is doing great work in the {industry} space. I wanted to reach out because I think {product} could help you {value_proposition}.</p>
            
            <p>Would you be open to a quick 15-minute call to explore how we might be able to help?</p>
        </div>
        
        <div class="signature">
            <p>Best regards,<br>
            <strong>{sender_name}</strong><br>
            {sender_title}</p>
        </div>
        
        <div class="footer">
            <p>If you'd prefer not to receive these emails, you can <a href="{unsubscribe_link}" class="unsubscribe">unsubscribe here</a>.</p>
        </div>
    </div>
</body>
</html>"""
)


FOLLOW_UP_1 = EmailTemplate(
    name="follow_up_1",
    subject="Re: Quick question about {company}",
    body_text="""Hi {name},

I wanted to follow up on my previous email about {product}.

I understand you're busy, but I genuinely believe we could help {company} with {value_proposition}.

Would you have 10 minutes this week for a quick call?

Best regards,
{sender_name}
{sender_title}

---
If you'd prefer not to receive these emails, you can unsubscribe here: {unsubscribe_link}""",
    
    body_html="""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .content {{ margin-bottom: 30px; }}
        .signature {{ margin-top: 30px; color: #666; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #999; }}
        .unsubscribe {{ color: #666; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <p>Hi {name},</p>
            
            <p>I wanted to follow up on my previous email about <strong>{product}</strong>.</p>
            
            <p>I understand you're busy, but I genuinely believe we could help {company} with {value_proposition}.</p>
            
            <p>Would you have 10 minutes this week for a quick call?</p>
        </div>
        
        <div class="signature">
            <p>Best regards,<br>
            <strong>{sender_name}</strong><br>
            {sender_title}</p>
        </div>
        
        <div class="footer">
            <p>If you'd prefer not to receive these emails, you can <a href="{unsubscribe_link}" class="unsubscribe">unsubscribe here</a>.</p>
        </div>
    </div>
</body>
</html>"""
)


FOLLOW_UP_2 = EmailTemplate(
    name="follow_up_2",
    subject="Last follow-up about {company}",
    body_text="""Hi {name},

This will be my last email - I don't want to be a bother!

I still think {product} could be valuable for {company}, especially when it comes to {value_proposition}.

If you're interested, just reply to this email and we can set up a quick call.

Otherwise, I wish you all the best with {company}!

Best regards,
{sender_name}
{sender_title}

---
If you'd prefer not to receive these emails, you can unsubscribe here: {unsubscribe_link}""",
    
    body_html="""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .content {{ margin-bottom: 30px; }}
        .signature {{ margin-top: 30px; color: #666; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #999; }}
        .unsubscribe {{ color: #666; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <p>Hi {name},</p>
            
            <p>This will be my last email - I don't want to be a bother!</p>
            
            <p>I still think <strong>{product}</strong> could be valuable for {company}, especially when it comes to {value_proposition}.</p>
            
            <p>If you're interested, just reply to this email and we can set up a quick call.</p>
            
            <p>Otherwise, I wish you all the best with {company}!</p>
        </div>
        
        <div class="signature">
            <p>Best regards,<br>
            <strong>{sender_name}</strong><br>
            {sender_title}</p>
        </div>
        
        <div class="footer">
            <p>If you'd prefer not to receive these emails, you can <a href="{unsubscribe_link}" class="unsubscribe">unsubscribe here</a>.</p>
        </div>
    </div>
</body>
</html>"""
)


# Template registry
TEMPLATES = {
    'initial': INITIAL_OUTREACH,
    'follow_up_1': FOLLOW_UP_1,
    'follow_up_2': FOLLOW_UP_2,
}


def get_template(template_name: str) -> EmailTemplate:
    """Get template by name"""
    if template_name not in TEMPLATES:
        raise ValueError(f"Template '{template_name}' not found. Available: {list(TEMPLATES.keys())}")
    return TEMPLATES[template_name]


def render_template(template_name: str, **kwargs) -> Dict[str, str]:
    """Render a template with provided variables"""
    template = get_template(template_name)
    return template.render(**kwargs)


def get_default_variables(
    company_name: str = "Your Company",
    contact_name: str = "there",
    industry: str = "technology",
    product: str = "our solution",
    value_proposition: str = "streamline your operations",
    sender_name: str = "Sales Team",
    sender_title: str = "Business Development",
    unsubscribe_link: str = "#"
) -> Dict[str, str]:
    """Get default template variables"""
    return {
        'company': company_name,
        'name': contact_name,
        'industry': industry,
        'product': product,
        'value_proposition': value_proposition,
        'sender_name': sender_name,
        'sender_title': sender_title,
        'unsubscribe_link': unsubscribe_link
    }
