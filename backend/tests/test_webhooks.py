import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.models import StripeEvent, User, Subscription
from app.stripe_webhook import is_event_processed, mark_event_processed, handle_checkout_session_completed
from app.security import hash_password

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_event_idempotency(session: Session):
    """Test that events are marked as processed and detected."""
    event_id = "evt_test_12345"
    
    # Should not be processed initially
    assert not is_event_processed(session, event_id)
    
    # Mark as processed
    mark_event_processed(session, event_id, "checkout.session.completed")
    
    # Should now be processed
    assert is_event_processed(session, event_id)
    
    # Verify it's in the database
    event = session.query(StripeEvent).filter(StripeEvent.stripe_event_id == event_id).first()
    assert event is not None
    assert event.event_type == "checkout.session.completed"

def test_duplicate_event_handling(session: Session):
    """Test that duplicate events are ignored."""
    event_id = "evt_test_duplicate"
    
    # Process once
    mark_event_processed(session, event_id, "test.event")
    
    # Try to process again
    mark_event_processed(session, event_id, "test.event")
    
    # Should only have one record
    events = session.query(StripeEvent).filter(StripeEvent.stripe_event_id == event_id).all()
    assert len(events) == 1

def test_checkout_completed_handler(session: Session):
    """Test checkout.session.completed handler."""
    # Create user
    user = User(email="test@example.com", password_hash=hash_password("password"))
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Simulate Stripe checkout session
    checkout_session = {
        "id": "cs_test_123",
        "customer_email": "test@example.com",
        "customer": "cus_test_123",
        "subscription": "sub_test_123",
        "metadata": {"plan": "pro_monthly"}
    }
    
    # Handle event
    handle_checkout_session_completed(session, checkout_session)
    
    # Verify subscription was created/updated
    sub = session.query(Subscription).filter(Subscription.user_id == user.id).first()
    assert sub is not None
    assert sub.stripe_customer_id == "cus_test_123"
    assert sub.stripe_subscription_id == "sub_test_123"
    assert sub.plan == "pro_monthly"
    assert sub.status == "active"

def test_checkout_completed_missing_user(session: Session):
    """Test checkout handler with non-existent user."""
    checkout_session = {
        "id": "cs_test_456",
        "customer_email": "nonexistent@example.com",
        "customer": "cus_test_456",
        "subscription": "sub_test_456",
        "metadata": {"plan": "pro_monthly"}
    }
    
    # Should not raise error, just log warning
    handle_checkout_session_completed(session, checkout_session)
    
    # No subscription should be created
    subs = session.query(Subscription).all()
    assert len(subs) == 0
