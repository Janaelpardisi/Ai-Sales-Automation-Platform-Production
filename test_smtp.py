"""
Simple SMTP Test - Send one test email
"""

import sys
sys.path.insert(0, 'backend')

import asyncio
from app.tools.email_sender import email_sender
from app.config import settings

async def test_smtp():
    """Test SMTP connection and send a simple email"""
    
    print("=" * 60)
    print("📧 TESTING SMTP CONNECTION")
    print("=" * 60)
    
    print(f"\n📋 SMTP Configuration:")
    print(f"   • Host: {settings.SMTP_HOST}")
    print(f"   • Port: {settings.SMTP_PORT}")
    print(f"   • User: {settings.SMTP_USER}")
    print(f"   • From: {settings.SMTP_FROM_EMAIL}")
    print(f"   • Password: {'*' * len(settings.SMTP_PASSWORD) if settings.SMTP_PASSWORD else 'NOT SET'}")
    
    # Test email details
    to_email = settings.SMTP_USER  # Send to yourself
    subject = "🧪 Test Email from AI Sales Agent"
    body_text = """
Hello!

This is a test email from the AI Sales Agent system.

If you're reading this, it means the email system is working correctly! 🎉

Best regards,
AI Sales Agent Team
    """
    
    body_html = """
<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
    <h2 style="color: #2563eb;">🧪 Test Email</h2>
    <p>Hello!</p>
    <p>This is a test email from the <strong>AI Sales Agent</strong> system.</p>
    <p>If you're reading this, it means the email system is working correctly! 🎉</p>
    <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
    <p style="color: #666; font-size: 14px;">
        Best regards,<br>
        AI Sales Agent Team
    </p>
</body>
</html>
    """
    
    print(f"\n📨 Sending test email to: {to_email}")
    print(f"   Subject: {subject}")
    
    try:
        success = await email_sender.send_email(
            to_email=to_email,
            subject=subject,
            body_text=body_text,
            body_html=body_html
        )
        
        if success:
            print("\n✅ SUCCESS! Email sent successfully!")
            print(f"\n📬 Check your inbox: {to_email}")
            print("   (It might take a few seconds to arrive)")
        else:
            print("\n❌ FAILED! Email was not sent.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print(f"\n🔍 Error details: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("\n💡 Common issues:")
        print("   1. Wrong password (make sure it's the Outlook password)")
        print("   2. Outlook blocking the connection")
        print("   3. Network/firewall issues")
        print("   4. SMTP settings incorrect")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_smtp())
