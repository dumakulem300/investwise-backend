import json
from app.config import settings
import firebase_admin
from firebase_admin import credentials, firestore

# Load the JSON file using the path returned by settings
cred_path = settings.get_firebase_credentials()
with open(cred_path, 'r') as f:
    cred_dict = json.load(f)

cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_db():
    return db