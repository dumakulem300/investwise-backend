import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    
    @classmethod
    def get_firebase_credentials(cls):
        for file in cls.PROJECT_ROOT.glob("*.json"):
            if "firebase" in file.name.lower() or "serviceaccount" in file.name.lower():
                return str(file)
        raise FileNotFoundError("No Firebase service account JSON found in backend folder")
    
    ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "admin@example.com").split(",")
    TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY", "")

settings = Settings()