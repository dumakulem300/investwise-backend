from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from google.cloud import firestore
import yfinance as yf
from firebase_admin import firestore as admin_firestore
import firebase_admin
from app.database import db as firestore_client
from app.auth import verify_firebase_token
from app.models import STOCKS_COLLECTION
from app.routers import stocks, news, lessons, subscription, admin
from app.services.lesson_service import seed_lessons_if_empty
from app.services.scheduler import start_scheduler, stop_scheduler, manual_refresh
from app.services.stock_service import get_latest_predictions_from_firestore

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: seed lessons
    seed_lessons_if_empty()
    # Start scheduler (daily 8 AM)
    start_scheduler()
    # Optionally run initial refresh if Firestore predictions are empty
    predictions = get_latest_predictions_from_firestore()
    if not any(p["price"] is not None for p in predictions):
        print("Initial data missing, running first refresh...")
        manual_refresh()
    yield
    # Shutdown: stop scheduler
    stop_scheduler()

app = FastAPI(title="InvestWise API", lifespan=lifespan)

# Configure CORS – allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",   # Vite default
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(stocks.router)
app.include_router(news.router)
app.include_router(lessons.router)
app.include_router(subscription.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "InvestWise API - Firebase"}

@app.get("/health")
async def health_check():
    try:
        doc_ref = firestore_client.collection("_test").document("ping")
        doc_ref.set({"ts": admin_firestore.SERVER_TIMESTAMP})
        db_status = "ok"
    except Exception as e:
        db_status = str(e)
    return {"status": "healthy", "firestore": db_status}

@app.get("/stocks/{symbol}")
async def get_stock(symbol: str, user=Depends(verify_firebase_token)):
    symbol = symbol.upper()
    stock_ref = firestore_client.collection(STOCKS_COLLECTION).document(symbol)
    stock_doc = stock_ref.get()
    if stock_doc.exists:
        data = stock_doc.to_dict()
        return {"symbol": symbol, "cached": True, **data}
    ticker = yf.Ticker(symbol)
    info = ticker.info
    stock_ref.set({
        "name": info.get("longName", symbol),
        "current_price": info.get("currentPrice", 0),
        "market_cap": info.get("marketCap", 0),
        "last_updated": admin_firestore.SERVER_TIMESTAMP
    })
    return {"symbol": symbol, "cached": False, "name": info.get("longName"), "price": info.get("currentPrice")}