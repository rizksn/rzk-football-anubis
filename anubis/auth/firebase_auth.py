import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends, Header
import os

# 🔐 Load service account key securely from env
FIREBASE_CRED_PATH = os.getenv("FIREBASE_ADMIN_CRED_PATH")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred)

def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # includes 'uid', 'email', 'name', etc.
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")