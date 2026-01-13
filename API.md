# Insight Atlas API Documentation

This document provides an overview of the Insight Atlas API endpoints, authentication, and examples.

-   **Base URL (Staging)**: `https://insight-atlas-api-staging.fly.dev`
-   **Base URL (Production)**: `https://insight-atlas-api.fly.dev`
-   **Interactive Docs**: Visit `/docs` on your deployed API for a full OpenAPI (Swagger) interface.

## 1. Authentication

All protected endpoints require a `Bearer` token in the `Authorization` header.

`Authorization: Bearer <your_jwt_token>`

Tokens are obtained via the `/auth/register` or `/auth/login` endpoints.

## 2. Endpoints

### Health & Version

-   `GET /healthz`: Health check. Returns `{"status": "ok"}`.
-   `GET /version`: API version. Returns `{"version": "0.2.0", "demo_mode": ...}`.

### Authentication

-   **`POST /auth/register`**: Create a new user account.
    -   **Body**: `{"email": "user@example.com", "password": "your_password"}`
    -   **Returns**: `{"access_token": "...", "token_type": "bearer"}`

-   **`POST /auth/login`**: Log in and get a new token.
    -   **Body**: `{"email": "user@example.com", "password": "your_password"}`
    -   **Returns**: `{"access_token": "...", "token_type": "bearer"}`

### User & Subscription

-   **`GET /me`**: Get current user and subscription info.
    -   **Auth**: Required.
    -   **Returns**: `{"email": "...", "plan": "...", "status": "..."}`

### Core Workflow

-   **`POST /intake`**: Create a new analysis session.
    -   **Auth**: Required (Pro plan).
    -   **Body**: `{"consent": true, "survey": {"..."}, "free_text": "..."}`
    -   **Returns**: `{"session_id": 123}`

-   **`POST /analyze/{session_id}`**: Run analysis on an intake session.
    -   **Auth**: Required (Pro plan).
    -   **Returns**: A full report object with scores and narrative.

-   **`GET /reports`**: List all past reports for the user.
    -   **Auth**: Required.
    -   **Returns**: A list of report objects.

### Billing

-   **`POST /billing/checkout`**: Get a Stripe Checkout URL.
    -   **Auth**: Required.
    -   **Query Params**: `?plan=monthly` or `?plan=yearly`
    -   **Returns**: `{"url": "https://checkout.stripe.com/..."}`

-   **`POST /stripe/webhook`**: Stripe webhook handler. Not for direct client use.

### Data Management

-   **`DELETE /data/purge`**: Delete all of the user's data (intakes and reports).
    -   **Auth**: Required.
    -   **Returns**: `{"ok": true}`

## 3. Examples

### Register and Analyze (cURL)

```bash
# 1. Register
TOKEN_JSON=$(curl -X POST "https://<api-url>/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}')

TOKEN=$(echo $TOKEN_JSON | jq -r .access_token)

# 2. Upgrade (in demo mode)
curl -X POST "https://<api-url>/billing/checkout?plan=monthly" \
  -H "Authorization: Bearer $TOKEN"

# 3. Create Intake Session
SESSION_JSON=$(curl -X POST "https://<api-url>/intake" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"consent":true,"survey":{"novelty_seeking":5},"free_text":"I enjoy building new systems."}')

SESSION_ID=$(echo $SESSION_JSON | jq -r .session_id)

# 4. Analyze
curl -X POST "https://<api-url>/analyze/$SESSION_ID" \
  -H "Authorization: Bearer $TOKEN"
```

### Using the CLI (`atlasctl.py`)

The `cli/atlasctl.py` script provides a convenient wrapper.

```bash
# Set environment variables
export ATLAS_API="https://<api-url>"
export ATLAS_TOKEN="<your-token>"

# Run a full flow
python3 cli/atlasctl.py register cli-user@example.com "password"
python3 cli/atlasctl.py billing monthly
SESSION_ID=$(python3 cli/atlasctl.py intake --consent --text "Test" | jq .session_id)
python3 cli/atlasctl.py analyze $SESSION_ID
```
