# Real World Email Lead Extractor with AI

An automated Python pipeline that connects to Gmail via IMAP, retrieves incoming unread leads, analyzes and extracts structured data using Google Gemini AI, and exports formatted JSON records.

---

## Features

- **Gmail IMAP Integration:** Securely fetches unread emails.
- **Gemini AI Lead Parsing:** Automatically extracts Name, Email, Company, Phone, Interest, and Urgency.
- **Secure Configuration:** Zero hardcoded credentials via `.env` management.
- **Structured Storage:** Saves lead data as localized JSON files for CRM/database integration.

---

## Project Structure

```text
├── email_fetcher.py     # Connects to Gmail and fetches unread messages
├── airead.py            # Sends email content to Gemini AI and parses JSON
├── requirements.txt     # Python dependencies
├── .env                 # API keys & Gmail credentials (ignored by Git)
├── .gitignore           # Excludes secrets & virtual environments
└── README.md            # Project documentation
Setup Instructions
1. Install Dependencies
pip install -r requirements.txt
2. Configure Environment Variables
Create a .env file in the project root folder:
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
GMAIL_USER="your_email@gmail.com"
GMAIL_APP_PASSWORD="your_16_digit_app_password"
Note: Generate a 16-character App Password under Google Account > Security > 2-Step Verification > App Passwords.
Usage
Run Full AI Extraction Pipeline
python airead.py
This fetches unread messages, analyzes them with Gemini AI, and outputs lead_1.json, lead_2.json, etc.
Fetch Emails Only (Inspection Mode)
Bash
python email_fetcher.py
Output Example
Generated JSON (lead_1.json):
{
  "original_email": {
    "sender": "client@example.com",
    "subject": "Enterprise Plan Inquiry",
    "body": "Hi, I would like to know pricing for 50 seats..."
  },
  "ai_extracted_data": {
    "name": "Alex Johnson",
    "email": "client@example.com",
    "company": "Nexus Corp",
    "phone": "+1-555-0199",
    "interest": "Enterprise tier pricing for 50 seats",
    "urgency": "High"
  }
}