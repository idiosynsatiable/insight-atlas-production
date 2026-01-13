# Insight Atlas (MVP)
A consent-first **self-understanding** portal that helps users explore communication style, cognitive preferences, and strengths
from short surveys + free-text. **Not a medical or psychological diagnostic tool.**

## What you get (working MVP)
- Next.js (frontend) + FastAPI (backend)
- Account creation + login (JWT)
- Session intake (survey + free text)
- Deterministic analysis engine (runs offline, no LLM required)
- Optional **LLM narrative polisher** (backend-only) to rewrite narrative while keeping scores deterministic
- Explainable report (features -> scores -> narrative)
- OpenAPI docs + CLI client
- Stripe integration (optional) with a real **DEMO MODE** fallback

## Quick start (Docker)
1. Install Docker + Docker Compose
2. From repo root:
```bash
docker compose up --build
```
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs

## Quick start (Local)
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment variables
Copy `.env.example` to `.env` in `backend/` and `frontend/` as needed.

### Backend (.env)
- `DATABASE_URL` (default uses SQLite file)
- `JWT_SECRET` (required)
- `STRIPE_SECRET_KEY` (optional)
- `STRIPE_WEBHOOK_SECRET` (optional)
- `DEMO_MODE=true` (bypasses paywall for testing)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE=http://localhost:8000`

## Manus integration
- OpenAPI: `backend/openapi.json` (generated at runtime as well)
- CLI: `cli/atlasctl.py`

## Safety / ethics
- Explicit consent gate before analysis
- No diagnosis; no claims like "you have autism"
- Reports are framed as *hypotheses* and *self-reflection aids*
- Data minimization + export/delete endpoints

