from __future__ import annotations
import stripe
from fastapi import Request, HTTPException
from sqlmodel import Session, select
from typing import Dict, Any
from .config import settings
from .models import Subscription, User, StripeEvent
import logging

logger = logging.getLogger(__name__)

def verify_webhook_signature(payload: bytes, sig_header: str) -> Dict[str, Any]:
    """Verify Stripe webhook signature and return event dict."""
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        return event
    except ValueError:
        logger.error("Invalid webhook payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid webhook signature")
        raise HTTPException(status_code=400, detail="Invalid signature")

def is_event_processed(db: Session, event_id: str) -> bool:
    """Check if event has already been processed."""
    existing = db.exec(select(StripeEvent).where(StripeEvent.stripe_event_id == event_id)).first()
    return existing is not None

def mark_event_processed(db: Session, event_id: str, event_type: str) -> None:
    """Mark event as processed for idempotency."""
    stripe_event = StripeEvent(stripe_event_id=event_id, event_type=event_type)
    db.add(stripe_event)
    db.commit()

def handle_checkout_session_completed(db: Session, session: Dict[str, Any]) -> None:
    """Handle checkout.session.completed event."""
    customer_email = session.get("customer_email")
    customer_id = session.get("customer")
    subscription_id = session.get("subscription")
    
    if not customer_email:
        logger.warning(f"No customer_email in checkout session {session.get('id')}")
        return
    
    # Find user by email
    user = db.exec(select(User).where(User.email == customer_email)).first()
    if not user:
        logger.warning(f"User not found for email {customer_email}")
        return
    
    # Update or create subscription
    sub = db.exec(select(Subscription).where(Subscription.user_id == user.id)).first()
    if not sub:
        sub = Subscription(user_id=user.id)
    
    sub.stripe_customer_id = customer_id
    sub.stripe_subscription_id = subscription_id
    sub.status = "active"
    
    # Determine plan from metadata or line items
    metadata = session.get("metadata", {})
    plan = metadata.get("plan", "pro_monthly")
    sub.plan = plan
    
    db.add(sub)
    db.commit()
    logger.info(f"Checkout completed for user {user.email}, plan {plan}")

def handle_subscription_updated(db: Session, subscription: Dict[str, Any]) -> None:
    """Handle customer.subscription.updated event."""
    subscription_id = subscription.get("id")
    status = subscription.get("status")
    
    # Find subscription by stripe_subscription_id
    sub = db.exec(select(Subscription).where(Subscription.stripe_subscription_id == subscription_id)).first()
    if not sub:
        logger.warning(f"Subscription not found for stripe_subscription_id {subscription_id}")
        return
    
    # Map Stripe status to our status
    if status in ("active", "trialing"):
        sub.status = "active"
    elif status in ("canceled", "incomplete_expired", "unpaid"):
        sub.status = "canceled"
        sub.plan = "free"
    
    db.add(sub)
    db.commit()
    logger.info(f"Subscription {subscription_id} updated to status {status}")

def handle_subscription_deleted(db: Session, subscription: Dict[str, Any]) -> None:
    """Handle customer.subscription.deleted event."""
    subscription_id = subscription.get("id")
    
    sub = db.exec(select(Subscription).where(Subscription.stripe_subscription_id == subscription_id)).first()
    if not sub:
        logger.warning(f"Subscription not found for stripe_subscription_id {subscription_id}")
        return
    
    sub.status = "canceled"
    sub.plan = "free"
    db.add(sub)
    db.commit()
    logger.info(f"Subscription {subscription_id} deleted")

def process_webhook_event(db: Session, event: Dict[str, Any]) -> None:
    """Process a verified webhook event."""
    event_id = event["id"]
    event_type = event["type"]
    
    # Check idempotency
    if is_event_processed(db, event_id):
        logger.info(f"Event {event_id} already processed, skipping")
        return
    
    # Route to handler
    data = event.get("data", {}).get("object", {})
    
    if event_type == "checkout.session.completed":
        handle_checkout_session_completed(db, data)
    elif event_type == "customer.subscription.updated":
        handle_subscription_updated(db, data)
    elif event_type == "customer.subscription.deleted":
        handle_subscription_deleted(db, data)
    else:
        logger.info(f"Unhandled event type: {event_type}")
    
    # Mark as processed
    mark_event_processed(db, event_id, event_type)
