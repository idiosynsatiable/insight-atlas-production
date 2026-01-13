# Insight Atlas - Live Deployment Guide

**Repository**: https://github.com/idiosynsatiable/insight-atlas-production

This guide provides step-by-step instructions to deploy Insight Atlas to production using **Railway** (backend) and **Vercel** (frontend).

---

## Part 1: Backend Deployment (Railway)

### Step 1: Create Railway Account & Project

1. Go to [Railway.app](https://railway.app) and sign up/login
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose `idiosynsatiable/insight-atlas-production`
5. Railway will detect the Dockerfile automatically

### Step 2: Configure Root Directory

1. In Railway project settings, click on your service
2. Go to **Settings** tab
3. Set **Root Directory** to: `backend`
4. Set **Start Command** to: `python -c "from app.db import init_db; init_db()" && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables

In Railway, go to **Variables** tab and add these:

```bash
# Database (Railway provides PostgreSQL)
DATABASE_URL=<railway-postgres-connection-string>

# Security
JWT_SECRET=<generate-with-openssl-rand-hex-32>

# Mode
DEMO_MODE=false

# CORS (will update after Vercel deployment)
CORS_ORIGINS=https://your-app.vercel.app

# App Base URL (will update after Vercel deployment)
APP_BASE_URL=https://your-app.vercel.app

# Stripe (use test keys first)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_PRO_MONTHLY=price_test_...
STRIPE_PRICE_YEARLY=price_test_...

# OpenAI (optional)
OPENAI_API_KEY=<your-key>
OPENAI_MODEL=gpt-4.1-mini
OPENAI_POLISH_ENABLED=true

# Rate Limiting
RATE_LIMIT_RPM=60

# Port (Railway auto-sets this)
PORT=${{PORT}}
```

### Step 4: Add PostgreSQL Database

1. In Railway project, click **"+ New"**
2. Select **"Database" → "PostgreSQL"**
3. Railway will auto-generate `DATABASE_URL`
4. Copy the connection string to your environment variables

### Step 5: Deploy

1. Click **"Deploy"** in Railway
2. Wait for build to complete (~3-5 minutes)
3. Once deployed, Railway will provide a public URL like: `https://your-app.up.railway.app`
4. Test the API: `curl https://your-app.up.railway.app/healthz`

---

## Part 2: Frontend Deployment (Vercel)

### Step 1: Import Project to Vercel

1. Go to [Vercel.com](https://vercel.com) and sign up/login
2. Click **"Add New..." → "Project"**
3. Import `idiosynsatiable/insight-atlas-production` from GitHub
4. Vercel will auto-detect Next.js

### Step 2: Configure Build Settings

1. **Root Directory**: Set to `frontend`
2. **Framework Preset**: Next.js (auto-detected)
3. **Build Command**: `pnpm build` (default)
4. **Install Command**: `pnpm install` (default)

### Step 3: Add Environment Variable

In Vercel project settings → **Environment Variables**:

```bash
NEXT_PUBLIC_API_BASE=https://your-app.up.railway.app
```

Replace `your-app.up.railway.app` with your actual Railway backend URL.

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for build (~2-3 minutes)
3. Vercel will provide a URL like: `https://insight-atlas-production.vercel.app`

### Step 5: Update Backend CORS

1. Go back to **Railway**
2. Update these environment variables:
   ```bash
   CORS_ORIGINS=https://insight-atlas-production.vercel.app
   APP_BASE_URL=https://insight-atlas-production.vercel.app
   ```
3. Railway will auto-redeploy

---

## Part 3: Stripe Configuration

### Step 1: Create Stripe Products

1. Log in to [Stripe Dashboard](https://dashboard.stripe.com)
2. Switch to **Test Mode** (toggle in top-right)
3. Go to **Products** → **Add Product**

**Product 1: Pro Monthly**
- Name: `Insight Atlas Pro Monthly`
- Price: `$19.00 USD` recurring monthly
- Copy the **Price ID** (starts with `price_`)

**Product 2: Pro Yearly**
- Name: `Insight Atlas Pro Yearly`
- Price: `$190.00 USD` recurring yearly
- Copy the **Price ID**

### Step 2: Get API Keys

1. Go to **Developers** → **API Keys**
2. Copy **Secret key** (starts with `sk_test_`)
3. Update Railway environment variable: `STRIPE_SECRET_KEY`

### Step 3: Configure Webhook

1. Go to **Developers** → **Webhooks**
2. Click **"Add endpoint"**
3. **Endpoint URL**: `https://your-app.up.railway.app/stripe/webhook`
4. **Events to send**:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Click **"Add endpoint"**
6. Copy the **Signing secret** (starts with `whsec_`)
7. Update Railway: `STRIPE_WEBHOOK_SECRET`

### Step 4: Update Price IDs in Railway

```bash
STRIPE_PRICE_PRO_MONTHLY=price_test_xxxxx
STRIPE_PRICE_YEARLY=price_test_yyyyy
```

---

## Part 4: Testing & Validation

### Test 1: Health Check

```bash
curl https://your-app.up.railway.app/healthz
# Expected: {"status":"ok"}
```

### Test 2: Frontend Loads

Visit `https://insight-atlas-production.vercel.app` in browser.

### Test 3: Full User Flow

1. **Register**: Go to `/app` and create account
2. **Upgrade**: Go to `/billing` and click "Upgrade Monthly"
3. **Stripe Checkout**: Use test card `4242 4242 4242 4242`
4. **Verify**: Check Railway logs for webhook event
5. **Test Pro Features**: Create intake session and analyze

### Test 4: Webhook Verification

```bash
# Check Railway logs
railway logs

# Look for:
# "Webhook received: checkout.session.completed"
# "Subscription updated for user..."
```

---

## Part 5: Go Live (Production)

### Switch to Live Mode

1. **Stripe**: Switch from Test Mode to Live Mode
   - Create new products with live prices
   - Get live API keys (`sk_live_...`)
   - Configure live webhook endpoint

2. **Railway**: Update environment variables
   ```bash
   DEMO_MODE=false
   STRIPE_SECRET_KEY=sk_live_...
   STRIPE_WEBHOOK_SECRET=whsec_live_...
   STRIPE_PRICE_PRO_MONTHLY=price_live_...
   STRIPE_PRICE_YEARLY=price_live_...
   ```

3. **Custom Domain** (Optional):
   - **Vercel**: Add custom domain in project settings
   - **Railway**: Add custom domain in service settings
   - Update `CORS_ORIGINS` and `APP_BASE_URL`

---

## Environment Variables Reference

### Backend (Railway)

| Variable | Example | Required |
|----------|---------|----------|
| `DATABASE_URL` | `postgresql://user:pass@host/db` | ✅ |
| `JWT_SECRET` | `<32-byte-hex-string>` | ✅ |
| `DEMO_MODE` | `false` | ✅ |
| `CORS_ORIGINS` | `https://app.vercel.app` | ✅ |
| `APP_BASE_URL` | `https://app.vercel.app` | ✅ |
| `STRIPE_SECRET_KEY` | `sk_test_...` or `sk_live_...` | ✅ |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` | ✅ |
| `STRIPE_PRICE_PRO_MONTHLY` | `price_...` | ✅ |
| `STRIPE_PRICE_YEARLY` | `price_...` | ✅ |
| `OPENAI_API_KEY` | `sk-...` | ❌ |
| `OPENAI_MODEL` | `gpt-4.1-mini` | ❌ |
| `OPENAI_POLISH_ENABLED` | `true` | ❌ |
| `RATE_LIMIT_RPM` | `60` | ❌ |
| `SENTRY_DSN` | `https://...@sentry.io/...` | ❌ |

### Frontend (Vercel)

| Variable | Example | Required |
|----------|---------|----------|
| `NEXT_PUBLIC_API_BASE` | `https://api.railway.app` | ✅ |

---

## Troubleshooting

### Backend won't start
- Check Railway logs: `railway logs`
- Verify `DATABASE_URL` is set correctly
- Ensure `PORT` variable is available

### CORS errors in browser
- Verify `CORS_ORIGINS` matches your Vercel URL exactly
- Check for trailing slashes (should not have them)
- Redeploy backend after changing CORS

### Stripe webhook not firing
- Check webhook URL is correct in Stripe dashboard
- Verify `STRIPE_WEBHOOK_SECRET` is set
- Test with Stripe CLI: `stripe trigger checkout.session.completed`

### Database connection failed
- Ensure PostgreSQL is running in Railway
- Check `DATABASE_URL` format
- Verify database is in same Railway project

---

## Live URLs (After Deployment)

- **Frontend**: `https://insight-atlas-production.vercel.app`
- **Backend API**: `https://your-app.up.railway.app`
- **API Docs**: `https://your-app.up.railway.app/docs`
- **GitHub Repo**: `https://github.com/idiosynsatiable/insight-atlas-production`

---

## SEO Optimization Included

✅ **Meta Tags**: Title, description, keywords for all pages  
✅ **Open Graph**: Social media preview cards  
✅ **Twitter Cards**: Twitter-specific metadata  
✅ **Structured Data**: JSON-LD schema for search engines  
✅ **Sitemap**: Auto-generated at `/sitemap.xml`  
✅ **Robots.txt**: Search engine crawling rules  
✅ **Semantic HTML**: Proper heading hierarchy and article tags  

---

## Security Checklist

- [ ] All secrets stored in Railway/Vercel (not in code)
- [ ] `DEMO_MODE=false` in production
- [ ] CORS locked to production domain
- [ ] Stripe webhook signature verification enabled
- [ ] JWT secret is strong random string
- [ ] PostgreSQL has strong password
- [ ] Rate limiting enabled

---

## Support

For issues or questions:
- Check `RUNBOOK.md` for debugging
- Review `SECURITY.md` for security practices
- See `API.md` for endpoint documentation

**Repository**: https://github.com/idiosynsatiable/insight-atlas-production
