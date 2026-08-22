import google.genai as genai
import json
import os
from dotenv import load_dotenv
from email_fetcher import fetch_unread_emails

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

client = genai.Client(api_key=API_KEY)

def analyze_email_with_ai(sender, subject, body):
    """Sends the email data to the AI and forces a JSON response."""
    
    system_prompt = """
    You are an AI assistant for a marketing agency. Your job is to read inbound emails, 
    determine if they are a potential client lead, and extract the key information.
    
    You MUST respond with a raw JSON object and nothing else. No markdown formatting, 
    no backticks, no explanations. Just the JSON.
    
    The JSON must match this exact structure:
    {
        "classification": "lead" or "not-lead",
        "confidence_score": (float between 0 and 1),
        "sender_email": "the email address",
        "project_type": "brief description of what they want (e.g., Social Media, Web Dev, SEO)",
        "summary": "A one or two sentence summary of the email",
        "budget_signal": "Any mention of budget or 'Unknown'"
    }
    """
    
    email_content = f"SENDER: {sender}\nSUBJECT: {subject}\nBODY: {body}"
    
    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',
            contents=system_prompt + "\n\n" + email_content
        )
        
        clean_json_string = response.text.strip("```json\n").strip("```").strip()
        return json.loads(clean_json_string)
        
    except Exception as e:
        print(f"Error processing email from {sender}: {e}")
        return None

if __name__ == "__main__":
    print("Checking for new leads...")
    new_emails = fetch_unread_emails()

    print(f"Fetched {len(new_emails)} new emails.\n")

    if new_emails:
        for i, email_data in enumerate(new_emails, 1):
            print(f"{'='*80}")
            print(f"Email #{i}")
            print(f"{'='*80}")
            print(f"From: {email_data['sender']}")
            print(f"Subject: {email_data['subject']}")
            print(f"\nBody:\n{email_data['body']}")
            print()
            
            print("Analyzing with AI...")
            ai_result = analyze_email_with_ai(
                sender=email_data['sender'],
                subject=email_data['subject'],
                body=email_data['body']
            )
            
            if ai_result:
                print("--- AI Analysis (CRM Ready) ---")
                print(json.dumps(ai_result, indent=4))
            print()
    else:
        print("No new emails to process.")