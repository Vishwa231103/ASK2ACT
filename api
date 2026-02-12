import os
import base64
import streamlit as st
from together import Together
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ===========================
# 1. Setup
# ===========================
st.set_page_config(page_title="Friday Email Summarizer", layout="centered")
st.title("📧 Friday - Email Summarizer")

# Together AI
client = Together(api_key="YOUR_TOGETHER_API_KEY")

# ===========================
# 2. Gmail API Connect
# ===========================
def get_gmail_service():
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.readonly"])
    service = build("gmail", "v1", credentials=creds)
    return service

# ===========================
# 3. Fetch Emails
# ===========================
def fetch_emails(max_results=5):
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", maxResults=max_results, labelIds=["INBOX"]).execute()
    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]
        subject = next(h["value"] for h in headers if h["name"] == "Subject")
        sender = next(h["value"] for h in headers if h["name"] == "From")

        # Get body
        body = ""
        if "data" in msg_data["payload"]["body"]:
            body = base64.urlsafe_b64decode(msg_data["payload"]["body"]["data"]).decode("utf-8", errors="ignore")

        emails.append({"subject": subject, "sender": sender, "body": body})
    return emails

# ===========================
# 4. Summarize with Together AI
# ===========================
def summarize_email(email_text):
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Friday, an AI email assistant. "
                    "Summarize emails into **short bullet points**. "
                    "Be concise, professional, and clear."
                )
            },
            {"role": "user", "content": email_text}
        ],
        max_tokens=150,
        temperature=0.5,
    )
    return response.choices[0].message.content

# ===========================
# 5. Streamlit UI
# ===========================
if st.button("📥 Summarize My Emails"):
    st.info("Fetching your inbox...")
    emails = fetch_emails(3)  # fetch 3 emails

    for i, email in enumerate(emails, start=1):
        st.subheader(f"📩 Email {i}: {email['subject']} (from {email['sender']})")
        summary = summarize_email(email["body"])
        st.write(summary)
