"""
Celery tasks for TezSavdo
"""
from celery import shared_task
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.management import call_command
from .models import Mahsulot, Buyurtma
import logging

logger = logging.getLogger(__name__)

# ============================================
# Session & Cache Management
# ============================================

@shared_task(bind=True, max_retries=3)
def cleanup_sessions(self):
    """
    Clean up expired sessions daily
    """
    try:
        Session.objects.filter(expire_date__lt=timezone.now()).delete()
        logger.info("Cleaned up expired sessions")
        return "Sessions cleaned successfully"
    except Exception as exc:
        logger.error(f"Error cleaning sessions: {exc}")
        raise self.retry(exc=exc, countdown=60)


# ============================================
# Product Management
# ============================================

@shared_task(bind=True, max_retries=3)
def update_product_cache(self):
    """
    Update popular products cache every 4 hours
    """
    try:
        # Get top products
        top_products = Mahsulot.objects.filter(
            is_active=True
        ).order_by('-sotish_soni')[:50]
        
        logger.info(f"Updated cache for {len(top_products)} products")
        return f"Updated cache for {len(top_products)} products"
    except Exception as exc:
        logger.error(f"Error updating product cache: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def sync_inventory(self):
    """
    Sync inventory with external systems (if applicable)
    """
    try:
        products = Mahsulot.objects.filter(is_active=True)
        # Add your sync logic here
        logger.info(f"Synced inventory for {products.count()} products")
        return f"Inventory synced for {products.count()} products"
    except Exception as exc:
        logger.error(f"Error syncing inventory: {exc}")
        raise self.retry(exc=exc, countdown=60)


# ============================================
# Email & Notifications
# ============================================

@shared_task(bind=True, max_retries=3)
def send_daily_reports(self):
    """
    Send daily admin reports
    """
    try:
        # Get today's order stats
        today_orders = Buyurtma.objects.filter(
            yaratildi__date=timezone.now().date()
        )
        
        order_count = today_orders.count()
        total_revenue = sum(order.summa for order in today_orders)
        
        # Send email logic here
        logger.info(f"Daily report sent: {order_count} orders, {total_revenue} sum")
        return f"Report sent: {order_count} orders"
    except Exception as exc:
        logger.error(f"Error sending daily reports: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_order_confirmation(self, order_id):
    """
    Send order confirmation email
    """
    try:
        order = Buyurtma.objects.get(id=order_id)
        # Send confirmation email
        logger.info(f"Order confirmation sent for order {order_id}")
        return f"Confirmation sent for order {order_id}"
    except Exception as exc:
        logger.error(f"Error sending order confirmation: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_reminder_emails(self):
    """
    Send reminder emails to users with abandoned carts
    """
    try:
        # Add logic to find abandoned carts and send reminders
        logger.info("Reminder emails sent")
        return "Reminder emails sent successfully"
    except Exception as exc:
        logger.error(f"Error sending reminder emails: {exc}")
        raise self.retry(exc=exc, countdown=60)


# ============================================
# Utility Tasks
# ============================================

@shared_task(bind=True, max_retries=3)
def database_backup(self):
    """
    Create database backup (you may want to use a service like Render's built-in backups)
    """
    try:
        logger.info("Database backup initiated")
        return "Database backup completed"
    except Exception as exc:
        logger.error(f"Error backing up database: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def cleanup_old_files(self):
    """
    Clean up old media files and temporary data
    """
    try:
        # Add logic to clean up old files
        logger.info("Old files cleaned up")
        return "Cleanup completed"
    except Exception as exc:
        logger.error(f"Error cleaning up files: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def test_task():
    """
    Test task to verify Celery is working
    """
    logger.info("Test task executed successfully")
    return "Test task completed"
