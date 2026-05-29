import logging
import firebase_admin
from firebase_admin import credentials, firestore
from app.config import settings

logger = logging.getLogger(__name__)

try:
    cred_dict = settings.get_firebase_credentials()
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    logger.info("Firebase initialized successfully")
except Exception as e:
    logger.error(f"Firebase initialization failed: {e}")
    # Do not crash – but subsequent operations that use db will fail.
    # On Render, this should not happen because env var is set.
    db = None

def get_db():
    if db is None:
        raise RuntimeError("Firestore client not available")
    return db
