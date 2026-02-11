# Gmail SMTP Setup Guide

## خطوات الحصول على Gmail App Password

### الخطوة 1: تفعيل المصادقة الثنائية (2FA)

1. افتح [Google Account](https://myaccount.google.com/)
2. اضغط على **Security** من القائمة الجانبية
3. في قسم "How you sign in to Google"
4. اضغط على **2-Step Verification**
5. اتبع الخطوات لتفعيل المصادقة الثنائية (هتحتاج رقم موبايل)

---

### الخطوة 2: إنشاء App Password

1. بعد تفعيل 2FA، ارجع لصفحة **Security**
2. في قسم "How you sign in to Google"
3. اضغط على **App passwords** (هتلاقيها تحت 2-Step Verification)
4. قد يطلب منك إدخال كلمة المرور مرة أخرى
5. في صفحة App passwords:
   - **Select app**: اختر "Mail"
   - **Select device**: اختر "Windows Computer" أو "Other (Custom name)"
   - اكتب اسم مثل "AI Sales Agent"
6. اضغط **Generate**
7. هيظهرلك **16-character password** (مثل: `abcd efgh ijkl mnop`)
8. **انسخ الباسورد ده** - مش هتقدر تشوفه تاني!

---

### الخطوة 3: تحديث ملف .env

افتح ملف `backend/.env` وحدث القيم التالية:

```env
# Email (Gmail SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-actual-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # الباسورد اللي نسخته (بدون مسافات)
SMTP_FROM_EMAIL=your-actual-email@gmail.com
SMTP_FROM_NAME=AI Sales Agent
```

**مثال:**
```env
SMTP_USER=ahmed.mohamed@gmail.com
SMTP_PASSWORD=xyzw abcd efgh ijkl  # 16 حرف
SMTP_FROM_EMAIL=ahmed.mohamed@gmail.com
SMTP_FROM_NAME=Ahmed Mohamed
```

---

### الخطوة 4: اختبار الإعدادات

بعد تحديث `.env`، شغل السيرفر واختبر:

```bash
cd backend
python -m app.main
```

ثم جرب إنشاء حملة وشوف لو الإيميلات بتتبعت!

---

## 🔗 روابط مفيدة

- **Google Account Security**: https://myaccount.google.com/security
- **App Passwords**: https://myaccount.google.com/apppasswords
- **2-Step Verification**: https://myaccount.google.com/signinoptions/two-step-verification

---

## ⚠️ ملاحظات مهمة

1. **App Password مش كلمة مرور Gmail العادية** - لازم تعمل واحد جديد
2. **لازم تفعل 2FA الأول** - مش هتقدر تعمل App Password بدونها
3. **الباسورد 16 حرف** - ممكن يكون فيه مسافات، شيلها لما تحطه في `.env`
4. **متشاركش الباسورد ده** - ده بيدي access كامل للإيميل
5. **لو نسيت الباسورد** - اعمل واحد جديد من نفس المكان

---

## 🧪 اختبار سريع

بعد ما تحط الـ credentials، جرب:

```bash
cd d:\Ai_Sales_Agent
python test_api.py
```

ده هيعمل campaign وهيبعت إيميلات للـ leads!
