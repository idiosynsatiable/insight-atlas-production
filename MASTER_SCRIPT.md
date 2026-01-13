# Master Script Checklist (Insight Atlas)

This file is the **single source-of-truth checklist** for repo/app/web builds:
- environments
- containers
- secrets
- CI/CD
- billing
- observability
- compliance (baseline)
- deployment

## Non-negotiables
- **No secrets in git** (keys/tokens belong in secret managers). See OpenAI key safety docs. 
- Explicit consent for any analysis.
- Explainability: features -> scores -> narrative.

## Environments
- local dev: docker compose
- staging: separate domain + separate secrets
- prod: separate domain + separate secrets

## Secrets (server-side only)
- OPENAI_API_KEY (backend only) citeturn0search1turn1search8
- STRIPE_SECRET_KEY + webhook secret (backend only)
- JWT_SECRET (backend only)

## CI/CD
- GitHub Actions CI: `.github/workflows/ci.yml`
- Deployment options:
  - API: Fly.io / Render / Railway / ECS
  - Web: Vercel / Netlify

## Billing
- Stripe Checkout subscriptions (monthly/yearly)
- Webhook handler (add next): activate/cancel plans

## Observability (add next)
- request id middleware
- structured logs
- error tracking (Sentry)

