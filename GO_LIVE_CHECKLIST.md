# Insight Atlas Go-Live Checklist

This checklist ensures all critical steps are completed before launching Insight Atlas to production.

## Pre-Deployment

### Infrastructure

- [ ] **PostgreSQL Database Provisioned**
  - [ ] Production database created
  - [ ] Staging database created
  - [ ] Connection strings obtained and tested
  - [ ] Backups configured

- [ ] **Fly.io Apps Created**
  - [ ] Production app: `insight-atlas-api`
  - [ ] Staging app: `insight-atlas-api-staging`
  - [ ] Health checks configured in `fly.toml`

- [ ] **Vercel Projects Configured**
  - [ ] Production project linked to `main` branch
  - [ ] Staging project linked to `develop` branch
  - [ ] Custom domains assigned

### Stripe Configuration

- [ ] **Production Stripe Account**
  - [ ] Products and prices created
  - [ ] Monthly price ID recorded
  - [ ] Yearly price ID recorded
  - [ ] Live mode API keys obtained
  - [ ] Webhook endpoint configured: `https://insight-atlas-api.fly.dev/stripe/webhook`
  - [ ] Webhook events enabled: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
  - [ ] Webhook signing secret recorded

- [ ] **Staging Stripe Account**
  - [ ] Test mode products and prices created
  - [ ] Test mode API keys obtained
  - [ ] Webhook endpoint configured: `https://insight-atlas-api-staging.fly.dev/stripe/webhook`

### Secrets Management

- [ ] **Backend Secrets Set (Production)**
  - [ ] `DATABASE_URL`
  - [ ] `JWT_SECRET` (generated with `openssl rand -hex 32`)
  - [ ] `DEMO_MODE=false`
  - [ ] `CORS_ORIGINS` (production frontend URL)
  - [ ] `APP_BASE_URL` (production frontend URL)
  - [ ] `STRIPE_SECRET_KEY` (live mode)
  - [ ] `STRIPE_WEBHOOK_SECRET`
  - [ ] `STRIPE_PRICE_PRO_MONTHLY`
  - [ ] `STRIPE_PRICE_YEARLY`
  - [ ] `OPENAI_API_KEY` (optional)
  - [ ] `SENTRY_DSN` (optional)

- [ ] **Backend Secrets Set (Staging)**
  - [ ] All secrets configured with staging/test values

- [ ] **Frontend Environment Variables**
  - [ ] `NEXT_PUBLIC_API_BASE` set for production
  - [ ] `NEXT_PUBLIC_API_BASE` set for staging

## Deployment

### Staging Deployment

- [ ] **Backend deployed to staging**
  - [ ] `fly deploy -a insight-atlas-api-staging` successful
  - [ ] Health check passes: `curl https://insight-atlas-api-staging.fly.dev/healthz`
  - [ ] Version endpoint accessible: `curl https://insight-atlas-api-staging.fly.dev/version`

- [ ] **Frontend deployed to staging**
  - [ ] Vercel deployment successful
  - [ ] Site loads without errors
  - [ ] Navigation works (App, Pricing, Billing)

- [ ] **Staging Smoke Test**
  - [ ] Run `master.sh` against staging API
  - [ ] Full flow works: register → upgrade → intake → analyze

### Production Deployment

- [ ] **Backend deployed to production**
  - [ ] `fly deploy -a insight-atlas-api` successful
  - [ ] Health check passes
  - [ ] Version endpoint shows `demo_mode: false`

- [ ] **Frontend deployed to production**
  - [ ] Vercel deployment successful
  - [ ] Custom domain resolves correctly
  - [ ] SSL certificate active

## Post-Deployment Validation

### Functional Testing

- [ ] **Authentication Flow**
  - [ ] User registration works
  - [ ] User login works
  - [ ] JWT token is valid

- [ ] **Billing Flow (Test Transaction)**
  - [ ] Upgrade button redirects to Stripe Checkout
  - [ ] Test payment completes successfully
  - [ ] Webhook fires and updates subscription in database
  - [ ] User gains Pro access immediately after payment

- [ ] **Core Workflow**
  - [ ] Pro user can create intake sessions
  - [ ] Analysis generates correct report structure
  - [ ] LLM polish works (if enabled)
  - [ ] Report export functions

- [ ] **Data Management**
  - [ ] Data purge endpoint works
  - [ ] User data is actually deleted from database

### Security Validation

- [ ] **CORS**
  - [ ] API rejects requests from unauthorized origins
  - [ ] Browser console shows no CORS errors on legitimate requests

- [ ] **Rate Limiting**
  - [ ] Excessive requests from single IP are throttled
  - [ ] Health endpoints are exempt

- [ ] **Webhook Security**
  - [ ] Invalid signature is rejected
  - [ ] Duplicate events are idempotent

### Monitoring & Observability

- [ ] **Logging**
  - [ ] Fly.io logs are accessible: `fly logs -a insight-atlas-api`
  - [ ] Request IDs appear in logs
  - [ ] Error logs are structured and readable

- [ ] **Sentry (if configured)**
  - [ ] Errors are captured and sent to Sentry
  - [ ] Alerts are configured for critical errors

- [ ] **Uptime Monitoring (optional)**
  - [ ] External uptime monitor configured (e.g., UptimeRobot, Pingdom)
  - [ ] Alerts configured for downtime

## Documentation

- [ ] **README.md updated** with production URLs
- [ ] **DEPLOYMENT.md** reviewed and accurate
- [ ] **SECURITY.md** reviewed
- [ ] **RUNBOOK.md** accessible to operations team
- [ ] **API.md** published or linked in README

## Legal & Compliance

- [ ] **Privacy Policy** published (if required)
- [ ] **Terms of Service** published (if required)
- [ ] **Consent language** reviewed for accuracy
- [ ] **"No diagnosis" disclaimers** present throughout UI

## Go-Live

- [ ] **Announcement prepared** (blog post, social media, email)
- [ ] **Support channel ready** (email, help desk)
- [ ] **Team briefed** on runbook and incident response
- [ ] **Rollback plan tested** (know how to revert both frontend and backend)

---

**Final Sign-Off**

- [ ] All checklist items completed
- [ ] Smoke test passed on production
- [ ] Team ready for launch

**Launch Date**: _______________

**Signed Off By**: _______________
