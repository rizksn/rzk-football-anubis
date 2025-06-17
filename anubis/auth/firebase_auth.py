import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends, Header

# 🔐 Try to load from Render secret file first, fallback to local path
cred_path = "/etc/secrets/firebase-adminsdk.json"

# If the Render-mounted secret file doesn't exist, fallback to local env var or dev path
if not os.path.exists(cred_path):
    cred_path = os.getenv("FIREBASE_ADMIN_CRED_PATH", "backend/secrets/firebase-adminsdk.json")

cred = credentials.Certificate(cred_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # contains uid, email, etc.
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")