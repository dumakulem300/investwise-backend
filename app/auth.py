from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()

async def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        )

async def get_current_user_uid(user_data: dict = Depends(verify_firebase_token)):
    uid = user_data.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="No uid in token")
    return uid

async def get_current_user_email(user_data: dict = Depends(verify_firebase_token)):
    email = user_data.get("email")
    logger.info(f"Extracted email from token: {email}")
    if not email:
        raise HTTPException(status_code=401, detail="No email in token")
    return email
