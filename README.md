# Real World Email Lead Extractor with AI

## Architecture

### Module 1: `email_fetcher.py`
- Connects to Gmail via IMAP
- Fetches unread emails
- Extracts: sender, subject, body

### Module 2: `ai_reader.py`  
- Imports emails from `email_fetcher.py`
- Analyzes with Google Gemini AI
- Extracts structured lead data (JSON)
- Saves results to `lead_*.json` files

---

## Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Google Gemini API Key
1. Go to: https://makersuite.google.com/app/apikeys
2. Click "Create API Key"
3. Copy the key
4. Open `ai_reader.py` and replace:
   ```python
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
   ```
   with your actual key

### Step 3: (Already Done) Gmail Setup
- Username and App Password are in `email_fetcher.py`
- IMAP is already enabled in your Gmail account

---

## Running the System

### Option 1: Run Full AI Analysis
```bash
python ai_reader.py
```
This will:
- Fetch all unread emails
- Analyze each with Gemini AI
- Extract lead data (name, email, company, phone, interest, urgency)
- Save to JSON files

### Option 2: Just Fetch Emails
```bash
python email_fetcher.py
```
This will:
- Fetch and display all unread emails
- Show sender, subject, body

---

## Output Example

**Console Output:**
```
================================================================================
REAL WORLD EMAIL LEAD EXTRACTOR - Using Google Gemini AI
================================================================================

Fetching emails from the integration module...
Connected. Selecting inbox...
Inbox selected. Searching unread messages...

Processing 2 emails with AI...

================================================================================
LEAD #1 - AI Analysis
================================================================================
From: john@company.com
Subject: Interested in your services

Sending to AI for analysis...
Extracted Lead Information:
----------------------------------------
  NAME: John Smith
  EMAIL: john@company.com
  COMPANY: Tech Corp Inc
  PHONE: +1-555-0123
  INTEREST: Pricing for enterprise package
  URGENCY: High

✓ Lead saved to: lead_1.json
```

**Saved JSON (`lead_1.json`):**
```json
{
  "original_email": {
    "sender": "john@company.com",
    "subject": "Interested in your services",
    "body": "..."
  },
  "ai_extracted_data": {
    "name": "John Smith",
    "email": "john@company.com",
    "company": "Tech Corp Inc",
    "phone": "+1-555-0123",
    "interest": "Pricing for enterprise package",
    "urgency": "High"
  }
}
```

---

## Next Steps (Task 3)
Send extracted leads to another person/system:
```python
def send_to_person_2(lead_data):
    # Could be: email, Slack message, database, webhook, etc.
    pass
```

---

## Troubleshooting

### "No new emails" or "Fetched 0 emails"
- Check Gmail inbox for unread emails
- Mark some emails as unread and try again

### "Invalid API Key" error
- Double-check your Gemini API key is correct
- Make sure it's not in a different environment

### Email body is empty
- Check email format (plain text vs HTML)
- Gmail might not be sending the body - this is expected for some emails

---

## Real World Use Case

This system is designed to:
1. **Automatically collect** incoming emails to your sales mailbox
2. **Parse lead information** using AI (no manual data entry!)
3. **Save structured data** for CRM/database integration
4. **Prioritize by urgency** set by AI analysis
5. **Forward to sales team** via email/Slack/API

Perfect for: **Inbound lead qualification and CRM automation**
