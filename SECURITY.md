 # Insight Atlas Security Guide

This document outlines the security practices and configurations for the Insight Atlas application.

## 1. Secrets Management

**Rule: No secrets are ever committed to the Git repository.**

All secrets, API keys, and sensitive configuration are managed through environment variables. These are injected into the deployment environments (Fly.io, Vercel) through their respective secrets management systems.

### Backend Secrets (Fly.io)

Secrets are set using the `fly secrets set` command. They are encrypted at rest and only available to the running application instances.

**Required Secrets:**

| Variable                   | Description                                       | Example                                    |
| -------------------------- | ------------------------------------------------- | ------------------------------------------ |
| `DATABASE_URL`             | Connection string for the PostgreSQL database.    | `postgresql://user:pass@host/db`           |
| `JWT_SECRET`               | A 256-bit random string for signing JWTs.         | (Use `openssl rand -hex 32` to generate)   |
| `STRIPE_SECRET_KEY`        | Your Stripe secret key (`sk_live_...` or `sk_test_...`). | `sk_live_...`                              |
| `STRIPE_WEBHOOK_SECRET`    | The signing secret for your Stripe webhook endpoint. | `whsec_...`                                |
| `STRIPE_PRICE_PRO_MONTHLY` | The Stripe Price ID for the monthly plan.         | `price_...`                                |
| `STRIPE_PRICE_YEARLY`      | The Stripe Price ID for the yearly plan.          | `price_...`                                |
| `OPENAI_API_KEY`           | (Optional) Your OpenAI API key.                   | `sk-...`                                   |
| `SENTRY_DSN`               | (Optional) Your Sentry DSN for error tracking.    | `https://...@sentry.io/...`                |

### Frontend Secrets (Vercel)

The frontend has no server-side secrets. The only environment variable is public.

| Variable                 | Description                         | Example                                  |
| ------------------------ | ----------------------------------- | ---------------------------------------- |
| `NEXT_PUBLIC_API_BASE`   | The base URL of the deployed backend. | `https://insight-atlas-api.fly.dev` |

## 2. Webhook Security

Stripe webhooks are critical for keeping subscription status in sync. We secure our webhook endpoint in two ways:

1.  **Signature Verification**: The `/stripe/webhook` endpoint verifies the `stripe-signature` header on every incoming request. The `STRIPE_WEBHOOK_SECRET` is used to validate that the request genuinely came from Stripe. Any request with an invalid signature is rejected with a `400 Bad Request` error.

2.  **Idempotency**: To prevent duplicate processing of the same event (e.g., due to network retries from Stripe), we store the ID of every successfully processed event in the `StripeEvent` database table. If an event with the same ID is received again, it is acknowledged with a `200 OK` but its handler logic is not re-executed.

## 3. Cross-Origin Resource Sharing (CORS)

The backend API is configured to only accept cross-origin requests from the authorized frontend domain. This is controlled by the `CORS_ORIGINS` environment variable.

-   **Local Development**: `http://localhost:3000`
-   **Staging**: `https://<your-staging-domain>.vercel.app`
-   **Production**: `https://<your-production-domain>.com`

Requests from any other origin will be blocked by the browser, preventing unauthorized websites from making requests to the API on behalf of a user.

## 4. Rate Limiting

To protect the API from abuse and ensure availability, we implement a simple in-memory rate limiter based on the client's IP address. This is configured via the `RATE_LIMIT_RPM` (requests per minute) environment variable.

-   **Default**: 60 requests per minute.
-   If a client exceeds this limit, they will receive a `429 Too Many Requests` error.
-   Health check endpoints (`/healthz`, `/version`) are exempt from rate limiting.

## 5. Authentication

-   User authentication is handled via JSON Web Tokens (JWT).
-   Tokens are signed with the `HS256` algorithm using the `JWT_SECRET`.
-   Tokens have a default expiration of 7 days.
-   Passwords are hashed using `bcrypt` before being stored in the database.
