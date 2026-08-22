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
            model='gemini-1.5-flash',
            contents=system_prompt + "\n\n" + email_content
        )
        
        clean_json_string = response.text.strip("```json\n").strip("```").strip()
        return json.loads(clean_json_string)
        
    except Exception as e:
        print(f"Error processing email from {sender}: {e}")
        return None

def main():
    print("Fetching new emails...")
    new_emails = fetch_unread_emails()
    
    if not new_emails:
        print("Inbox zero! No new emails to process.")
        return
        
    print(f"Found {len(new_emails)} new emails. Sending to AI for analysis...\n")
    
    for email_data in new_emails:
        print(f"Analyzing email from: {email_data['sender']}...")
        
        ai_result = analyze_email_with_ai(
            sender=email_data['sender'],
            subject=email_data['subject'],
            body=email_data['body']
        )
        
        if ai_result:
            print("--- AI Output for Person 2 (CRM Ready) ---")
            print(json.dumps(ai_result, indent=4))
            print("-" * 40 + "\n")

if __name__ == "__main__":
    main()