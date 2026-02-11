"""
Simple SMTP Test - Direct Connection to Mailtrap
"""
import asyncio
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def test_mailtrap():
    print("=" * 60)
    print("🧪 Testing Mailtrap SMTP Connection")
    print("=" * 60)
    
    # Mailtrap credentials
    smtp_host = "sandbox.smtp.mailtrap.io"
    smtp_port = 587
    smtp_user = "da59061b36dce5"
    smtp_password = "87de8077ae491b"
    
    print(f"\n📧 SMTP Settings:")
    print(f"   Host: {smtp_host}")
    print(f"   Port: {smtp_port}")
    print(f"   User: {smtp_user}")
    print(f"   Password: {'*' * len(smtp_password)}")
    
    # Create test email
    message = MIMEMultipart('alternative')
    message['Subject'] = "🧪 Test Email from AI Sales Agent"
    message['From'] = "AI Sales Agent <test@aisalesagent.com>"
    message['To'] = "test@example.com"
    
    body_text = "This is a test email from AI Sales Agent.\n\nIf you see this, SMTP is working! 🎉"
    part1 = MIMEText(body_text, 'plain')
    message.attach(part1)
    
    print(f"\n📨 Sending test email...")
    print(f"   From: {message['From']}")
    print(f"   To: {message['To']}")
    print(f"   Subject: {message['Subject']}")
    
    try:
        # Send email
        await aiosmtplib.send(
            message,
            hostname=smtp_host,
            port=smtp_port,
            username=smtp_user,
            password=smtp_password,
            start_tls=True,
        )
        
        print(f"\n✅ SUCCESS! Email sent successfully!")
        print(f"\n📬 Check your Mailtrap inbox:")
        print(f"   https://mailtrap.io/inboxes")
        print(f"\nYou should see the test email there! 🎉")
        
    except Exception as e:
        print(f"\n❌ FAILED! Error: {str(e)}")
        print(f"\nPossible issues:")
        print(f"   1. Firewall blocking port {smtp_port}")
        print(f"   2. Wrong credentials")
        print(f"   3. Network connection problem")
        return False
    
    print("\n" + "=" * 60)
    return True

if __name__ == "__main__":
    asyncio.run(test_mailtrap())
