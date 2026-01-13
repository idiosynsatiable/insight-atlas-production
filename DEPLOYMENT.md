# Insight Atlas Deployment Guide

This guide provides step-by-step instructions for deploying the Insight Atlas application to staging and production environments. The stack consists of a Next.js frontend deployed on Vercel and a FastAPI backend on Fly.io, with a PostgreSQL database.

## 1. Prerequisites

Before you begin, ensure you have the following:

- **Accounts**:
  - [GitHub](https://github.com/) account with access to the repository.
  - [Vercel](https://vercel.com/) account.
  - [Fly.io](https://fly.io/) account and `flyctl` CLI installed.
  - [Stripe](https://stripe.com/) account.
  - A managed PostgreSQL provider (e.g., Neon, Supabase, Aiven, or Fly Postgres).
- **Tools**:
  - `git`
  - `flyctl` (Fly.io CLI)
  - `vercel` (Vercel CLI, optional)

## 2. Environment Setup (Staging & Production)

The process is identical for both staging and production, but uses separate resources (domains, databases, API keys). Repeat these steps for each environment.

### 2.1. Provision PostgreSQL Database

1.  **Create a new database** from your chosen provider.
2.  Create two separate databases: `insight_atlas_staging` and `insight_atlas_prod`.
3.  Obtain the connection string for each. It will look like this:
    ```
    postgresql://<user>:<password>@<host>:<port>/<database_name>
    ```

### 2.2. Configure Stripe

1.  **Create two new Stripe projects**: one for staging (in test mode) and one for production (in live mode).
2.  For each project, create your products and prices:
    -   **Product**: Insight Atlas Pro
    -   **Prices**: Create two prices for this product:
        -   A monthly recurring price (e.g., $19/month).
        -   A yearly recurring price (e.g., $190/year).
3.  **Record the Price IDs** for both monthly and yearly plans (e.g., `price_...`).
4.  **Get API Keys**: Find your secret key (`sk_...`) and webhook signing secret (`whsec_...`).

## 3. Backend Deployment (Fly.io)

These steps deploy the FastAPI backend.

### 3.1. Initial Setup

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd insight-atlas-prod/backend
    ```
2.  **Launch the app on Fly.io**:
    -   For production: `fly launch --name insight-atlas-api`
    -   For staging: `fly launch --name insight-atlas-api-staging`
    This will create a `fly.toml` file and a new app on your Fly.io dashboard.

### 3.2. Set Secrets

Use the `fly secrets set` command to configure the environment variables. **These are not stored in your code.**

**Staging Example:**
```bash
fly secrets set -a insight-atlas-api-staging \
  DATABASE_URL="<your-staging-postgres-url>" \
  JWT_SECRET="<generate-a-strong-random-secret>" \
  DEMO_MODE="false" \
  CORS_ORIGINS="https://<your-staging-vercel-domain>.vercel.app" \
  APP_BASE_URL="https://<your-staging-vercel-domain>.vercel.app" \
  STRIPE_SECRET_KEY="sk_test_..." \
  STRIPE_WEBHOOK_SECRET="whsec_..." \
  STRIPE_PRICE_PRO_MONTHLY="price_test_..." \
  STRIPE_PRICE_YEARLY="price_test_..."
```

**Production Example:**
```bash
fly secrets set -a insight-atlas-api \
  DATABASE_URL="<your-production-postgres-url>" \
  JWT_SECRET="<generate-a-different-strong-secret>" \
  DEMO_MODE="false" \
  CORS_ORIGINS="https://<your-production-domain>.com" \
  APP_BASE_URL="https://<your-production-domain>.com" \
  STRIPE_SECRET_KEY="sk_live_..." \
  STRIPE_WEBHOOK_SECRET="whsec_..." \
  STRIPE_PRICE_PRO_MONTHLY="price_live_..." \
  STRIPE_PRICE_YEARLY="price_live_..."
```

### 3.3. Deploy

1.  **Run the deploy command**:
    ```bash
    fly deploy -a <your-fly-app-name>
    ```
2.  **Check the status**: `fly status -a <your-fly-app-name>`
3.  The API will be available at `https://<your-fly-app-name>.fly.dev`.

## 4. Frontend Deployment (Vercel)

These steps deploy the Next.js frontend.

### 4.1. Import Project

1.  Log in to your Vercel dashboard.
2.  Click **Add New...** > **Project**.
3.  Import your forked GitHub repository.
4.  Vercel will automatically detect it as a Next.js project.

### 4.2. Configure Environment

1.  In the project settings, go to the **Environment Variables** section.
2.  Add the following variable:

| Name                   | Staging Value                                     | Production Value                                |
| ---------------------- | ------------------------------------------------- | ----------------------------------------------- |
| `NEXT_PUBLIC_API_BASE` | `https://insight-atlas-api-staging.fly.dev` | `https://insight-atlas-api.fly.dev` |

3.  **Assign Domains**: Connect your custom domains for staging and production in the **Domains** section.

### 4.3. Deploy

-   **Production**: Merges to the `main` branch will automatically trigger a production deployment.
-   **Staging**: Merges to the `develop` branch (or your chosen staging branch) will trigger a staging deployment.

## 5. Post-Deployment Checklist

1.  **Configure Stripe Webhook Endpoint**:
    -   Go to your Stripe dashboard > Developers > Webhooks.
    -   Click **Add endpoint**.
    -   **Endpoint URL**: `https://<your-fly-app-name>.fly.dev/stripe/webhook`
    -   **Events to send**: Click "Select events" and add:
        -   `checkout.session.completed`
        -   `customer.subscription.updated`
        -   `customer.subscription.deleted`
    -   Click **Add endpoint**. Use the generated signing secret as your `STRIPE_WEBHOOK_SECRET`.

2.  **Run Smoke Test**: Use the `master.sh` script locally, but point it to your live staging or production URLs to verify the full flow.
    ```bash
    API_URL=https://<your-fly-app-name>.fly.dev ./master.sh
    ```

3.  **Verify CORS**: Open your browser's developer tools on your live frontend and ensure there are no CORS errors when making API requests.

4.  **Check Billing Flow**: Perform a real test transaction in your staging environment and a real purchase in production to ensure the entire billing and entitlement flow works correctly updates workflo w works correctly works correctly.
