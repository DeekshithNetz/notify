import os
import json
import firebase_admin
from firebase_admin import credentials, messaging

if os.path.exists("firebase_key.json"):
    # Local development
    cred = credentials.Certificate("firebase_key.json")
else:
    # Render
    firebase_credentials = json.loads(os.environ["FIREBASE_CREDENTIALS"])
    cred = credentials.Certificate(firebase_credentials)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def send_push_notification(token: str, title: str, body: str):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    response = messaging.send(message)
    return response