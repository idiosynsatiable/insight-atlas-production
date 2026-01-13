from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    plan: str = Field(default="free")  # free|pro_monthly|pro_yearly
    status: str = Field(default="active")  # active|canceled
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SessionIntake(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    consent: bool = Field(default=False)
    survey_json: str = Field(default="{}")
    free_text: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    session_id: int = Field(index=True)
    result_json: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StripeEvent(SQLModel, table=True):
    """Track processed Stripe webhook events for idempotency."""
    id: Optional[int] = Field(default=None, primary_key=True)
    stripe_event_id: str = Field(index=True, unique=True)
    event_type: str
    processed_at: datetime = Field(default_factory=datetime.utcnow)
