import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Header
from dotenv import load_dotenv

load_dotenv()

# Prefer production mount, fallback to env var or default
cred_path = "/etc/secrets/firebase-adminsdk.json"
if not os.path.exists(cred_path):
    cred_path = os.getenv("FIREBASE_ADMIN_CRED_PATH", "secrets/firebase-adminsdk.json")

if not os.path.exists(cred_path):
    raise RuntimeError(f"Firebase credential not found at {cred_path}")

cred = credentials.Certificate(cred_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = authorization.split(" ")[1]
    try:
        return auth.verify_id_token(token)  # contains uid, email, etc.
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
