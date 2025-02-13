import os
import pickle
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from flask import Flask, request, jsonify

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

app = Flask(__name__)

# Gmail Authentication
def gmail_authenticate():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:/Users/Tamil Adhavan/Downloads/racksecure_gmail_api_cred.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("gmail", "v1", credentials=creds)

# Function to send email
def send_email(subject, message, to_email):
    service = gmail_authenticate()
    email_msg = f"Subject: {subject}\n\n{message}"
    message = {"raw": email_msg.encode("utf-8").hex()}
    send_message = service.users().messages().send(userId="me", body=message).execute()
    return send_message

@app.route("/send_email", methods=["POST"])
def trigger_email():
    data = request.json
    product = data["product"]
    new_price = data["newPrice"]
    subject = "Price Drop Alert!"
    message = f"The price of {product} has been reduced to Rs {new_price}."
    send_email(subject, message, "receiver@example.com")
    return jsonify({"status": "Email Sent"}), 200

if __name__ == "__main__":
    app.run(debug=True)
