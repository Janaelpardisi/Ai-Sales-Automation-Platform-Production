"""
Test Email Templates
"""

import sys
sys.path.insert(0, 'backend')

from app.utils.email_templates import get_template, render_template, get_default_variables

print("=" * 70)
print("🧪 TESTING EMAIL TEMPLATES")
print("=" * 70)

# Test 1: Get template
print("\n📋 Test 1: Get Initial Template")
print("-" * 70)
try:
    template = get_template('initial')
    print(f"✅ Template Name: {template.name}")
    print(f"✅ Subject: {template.subject}")
    print(f"✅ Has HTML: {len(template.body_html) > 0}")
    print(f"✅ Has Text: {len(template.body_text) > 0}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Render template
print("\n📝 Test 2: Render Template with Variables")
print("-" * 70)
try:
    variables = get_default_variables(
        company_name="TechCorp Solutions",
        contact_name="Ahmed",
        industry="SaaS",
        product="AI Sales Agent",
        value_proposition="automate your lead generation and save 10+ hours per week",
        sender_name="Mohamed Ali",
        sender_title="Sales Director",
        unsubscribe_link="http://localhost:8000/unsubscribe?token=abc123"
    )
    
    rendered = render_template('initial', **variables)
    
    print(f"✅ Subject: {rendered['subject']}")
    print(f"\n✅ Text Body:\n{rendered['body_text'][:300]}...")
    print(f"\n✅ HTML Body Length: {len(rendered['body_html'])} characters")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: All templates
print("\n📋 Test 3: List All Templates")
print("-" * 70)
try:
    from app.utils.email_templates import TEMPLATES
    for name, template in TEMPLATES.items():
        print(f"✅ {name}: {template.subject}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Render follow-up templates
print("\n📧 Test 4: Render Follow-up Templates")
print("-" * 70)
try:
    for template_name in ['follow_up_1', 'follow_up_2']:
        rendered = render_template(template_name, **variables)
        print(f"✅ {template_name}: {rendered['subject']}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("✨ TEMPLATE TESTING COMPLETE!")
print("=" * 70)
