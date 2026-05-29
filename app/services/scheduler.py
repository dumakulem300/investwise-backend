from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import logging
from app.services.stock_data_fetcher import update_predictions

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Manila'))

def refresh_all_data():
    """Fetch real stock data and update Firestore predictions."""
    logger.info("Running scheduled refresh of stock predictions...")
    try:
        update_predictions()
        logger.info("Scheduled refresh completed successfully.")
    except Exception as e:
        logger.error(f"Scheduled refresh failed: {e}")

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            refresh_all_data,
            trigger=CronTrigger(hour=18, minute=0, timezone=pytz.timezone('Asia/Manila')),  # 6 PM PHT
            id='daily_refresh',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Scheduler started. Daily refresh at 6:00 PM PHT.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped.")

def manual_refresh():
    logger.info("Manual refresh triggered by admin.")
    refresh_all_data()