from __future__ import annotations
import stripe
from typing import Optional
from .config import settings

def stripe_configured() -> bool:
    return bool(settings.STRIPE_SECRET_KEY)

def init_stripe():
    if settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(customer_email: str, price_id: str, success_url: str, cancel_url: str, metadata: dict = None) -> str:
    init_stripe()
    session = stripe.checkout.Session.create(
        mode="subscription",
        customer_email=customer_email,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata or {},
    )
    return session.url
