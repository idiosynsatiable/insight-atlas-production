from __future__ import annotations
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import Optional, Dict, Any
import json
import logging
from .config import settings
from .db import init_db, get_session
from .models import User, SessionIntake, Report, Subscription
from .schemas import RegisterIn, LoginIn, TokenOut, IntakeIn, IntakeOut, ReportOut, MeOut
from .security import hash_password, verify_password, create_access_token, decode_token
from .analysis_engine import analyze
from .llm_polisher import polish_narrative
from .stripe_pay import stripe_configured, create_checkout_session
from .stripe_webhook import verify_webhook_signature, process_webhook_event
from .middleware import RequestIDMiddleware, RateLimitMiddleware, LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Insight Atlas API", version="0.2.0")

# Middleware stack (order matters)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, rpm=settings.RATE_LIMIT_RPM)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()
    logger.info("Insight Atlas API started")

# Health and version endpoints
@app.get("/healthz")
def healthz():
    """Health check endpoint for load balancers."""
    return {"status": "ok"}

@app.get("/version")
def version():
    """Version endpoint."""
    return {"version": "0.2.0", "demo_mode": settings.DEMO_MODE}

def _get_user_from_token(db: Session, authorization: Optional[str]) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    sub = decode_token(token, settings.JWT_SECRET)
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.exec(select(User).where(User.email == sub)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def _ensure_subscription_row(db: Session, user: User) -> Subscription:
    sub = db.exec(select(Subscription).where(Subscription.user_id == user.id)).first()
    if not sub:
        sub = Subscription(user_id=user.id, plan="free", status="active")
        db.add(sub)
        db.commit()
        db.refresh(sub)
    return sub

def _require_pro(db: Session, user: User) -> Subscription:
    sub = _ensure_subscription_row(db, user)
    if settings.DEMO_MODE:
        return sub
    if sub.plan.startswith("pro") and sub.status == "active":
        return sub
    raise HTTPException(status_code=402, detail="Upgrade required")

@app.post("/auth/register", response_model=TokenOut)
def register(payload: RegisterIn, db: Session = Depends(get_session)):
    existing = db.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    _ensure_subscription_row(db, user)
    token = create_access_token(user.email, settings.JWT_SECRET)
    logger.info(f"User registered: {user.email}")
    return TokenOut(access_token=token)

@app.post("/auth/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.email, settings.JWT_SECRET)
    return TokenOut(access_token=token)

@app.get("/me", response_model=MeOut)
def me(authorization: Optional[str] = Header(default=None), db: Session = Depends(get_session)):
    user = _get_user_from_token(db, authorization)
    sub = _ensure_subscription_row(db, user)
    return MeOut(email=user.email, plan=sub.plan, status=sub.status)

@app.post("/intake", response_model=IntakeOut)
def create_intake(payload: IntakeIn, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_session)):
    user = _get_user_from_token(db, authorization)
    if not payload.consent:
        raise HTTPException(status_code=400, detail="Consent required")
    _require_pro(db, user)
    s = SessionIntake(user_id=user.id, consent=True, survey_json=json.dumps(payload.survey), free_text=payload.free_text)
    db.add(s)
    db.commit()
    db.refresh(s)
    return IntakeOut(session_id=s.id)

@app.post("/analyze/{session_id}", response_model=ReportOut)
def analyze_session(session_id: int, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_session)):
    user = _get_user_from_token(db, authorization)
    _require_pro(db, user)
    s = db.exec(select(SessionIntake).where(SessionIntake.id == session_id, SessionIntake.user_id == user.id)).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    survey = json.loads(s.survey_json or "{}")
    result = analyze(s.free_text or "", survey)
    result = polish_narrative(result)
    r = Report(user_id=user.id, session_id=s.id, result_json=json.dumps(result))
    db.add(r)
    db.commit()
    db.refresh(r)
    return ReportOut(report_id=r.id, session_id=s.id, result=result)

@app.get("/reports", response_model=list[ReportOut])
def list_reports(authorization: Optional[str] = Header(default=None), db: Session = Depends(get_session)):
    user = _get_user_from_token(db, authorization)
    rows = db.exec(select(Report).where(Report.user_id == user.id).order_by(Report.created_at.desc())).all()
    out = []
    for r in rows:
        out.append(ReportOut(report_id=r.id, session_id=r.session_id, result=json.loads(r.result_json)))
    return out

@app.delete("/data/purge")
def purge_my_data(authorization: Optional[str] = Header(default=None), db: Session = Depends(get_session)):
    user = _get_user_from_token(db, authorization)
    # Delete reports + intakes. Keep account (user can delete via admin in MVP)
    reports = db.exec(select(Report).where(Report.user_id == user.id)).all()
    for r in reports:
        db.delete(r)
    intakes = db.exec(select(SessionIntake).where(SessionIntake.user_id == user.id)).all()
    for s in intakes:
        db.delete(s)
    db.commit()
    logger.info(f"Data purged for user {user.email}")
    return {"ok": True}

@app.post("/billing/checkout")
def billing_checkout(plan: str, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_session)):
    user = _get_user_from_token(db, authorization)
    if settings.DEMO_MODE:
        # Demo mode: upgrade plan in DB
        sub = _ensure_subscription_row(db, user)
        sub.plan = "pro_monthly" if plan == "monthly" else "pro_yearly"
        sub.status = "active"
        db.add(sub)
        db.commit()
        logger.info(f"Demo upgrade for {user.email} to {sub.plan}")
        return {"mode": "demo", "upgraded": True, "plan": sub.plan}

    if not stripe_configured():
        raise HTTPException(status_code=500, detail="Stripe not configured")
    price_id = settings.STRIPE_PRICE_PRO_MONTHLY if plan == "monthly" else settings.STRIPE_PRICE_YEARLY
    if not price_id:
        raise HTTPException(status_code=500, detail="Price id missing")
    
    # Use APP_BASE_URL for success/cancel URLs
    success_url = f"{settings.APP_BASE_URL}/billing/success"
    cancel_url = f"{settings.APP_BASE_URL}/billing/cancel"
    
    url = create_checkout_session(
        customer_email=user.email,
        price_id=price_id,
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"plan": f"pro_{plan}"}
    )
    return {"url": url}

@app.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_session)):
    """Handle Stripe webhook events with signature verification and idempotency."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing signature")
    
    event = verify_webhook_signature(payload, sig_header)
    
    try:
        process_webhook_event(db, event)
        return {"received": True}
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")
