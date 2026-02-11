# Quick Start Guide

Get AI Sales Agent up and running in 5 minutes!

## Prerequisites

- Python 3.9+
- Gmail account
- Google Gemini API key

## Installation Steps

### 1. Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ai-sales-agent.git
cd ai-sales-agent

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
playwright install
```

### 3. Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
# Required:
# - GEMINI_API_KEY
# - SMTP_USER
# - SMTP_PASSWORD
```

### 4. Get API Keys

**Gemini API Key:**
1. Visit https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy to `GEMINI_API_KEY` in `.env`

**Gmail App Password:**
1. Enable 2FA on Google Account
2. Visit https://myaccount.google.com/apppasswords
3. Generate app password
4. Copy to `SMTP_PASSWORD` in `.env`

See [GMAIL_SETUP_GUIDE.md](GMAIL_SETUP_GUIDE.md) for detailed instructions.

### 5. Run Application

```bash
# Start backend
cd backend
python -m app.main

# In another terminal, serve frontend
cd frontend
python -m http.server 8080
```

### 6. Access Dashboard

- Frontend: http://localhost:8080
- API Docs: http://localhost:8000/docs

## Using Docker (Alternative)

```bash
# Copy environment file
cp .env.docker.example .env

# Edit .env with your credentials

# Start services
docker-compose up -d

# Access at http://localhost:8080
```

## First Campaign

1. Open http://localhost:8080
2. Click "Create New Campaign"
3. Fill in:
   - Name: "Test Campaign"
   - Industry: "SaaS"
   - Location: "USA"
4. Click "Create Campaign"
5. Click "Run Campaign"
6. Watch leads appear!

## Troubleshooting

**Email not sending?**
- Check SMTP credentials in `.env`
- Verify Gmail app password (not regular password)
- Check logs in `backend/logs/`

**Gemini API errors?**
- Verify API key is correct
- Check API quota limits
- Ensure internet connection

**Database errors?**
- Check `DATA_DIR` path exists
- Verify write permissions
- Delete `data/sales_agent.db` and restart

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [API docs](http://localhost:8000/docs)
- Join discussions on GitHub
- Star the repo!

## Need Help?

- [Full Documentation](README.md)
- [Report Issues](https://github.com/yourusername/ai-sales-agent/issues)
- [Discussions](https://github.com/yourusername/ai-sales-agent/discussions)

---

Happy lead hunting!
