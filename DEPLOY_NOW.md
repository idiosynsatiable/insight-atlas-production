# 🚀 ONE-CLICK DEPLOYMENT GUIDE

## Step 1: Deploy Backend to Railway (2 minutes)

### Click This Button:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/idiosynsatiable/insight-atlas-production&envs=JWT_SECRET,DEMO_MODE,CORS_ORIGINS,APP_BASE_URL,STRIPE_SECRET_KEY,STRIPE_WEBHOOK_SECRET,STRIPE_PRICE_PRO_MONTHLY,STRIPE_PRICE_YEARLY&JWT_SECRETDesc=Generate+with:+openssl+rand+-hex+32&DEMO_MODEDesc=Set+to+false+for+production&CORS_ORIGINSDesc=Your+Vercel+frontend+URL&APP_BASE_URLDesc=Your+Vercel+frontend+URL&STRIPE_SECRET_KEYDesc=From+Stripe+Dashboard&STRIPE_WEBHOOK_SECRETDesc=From+Stripe+Webhook+Settings&STRIPE_PRICE_PRO_MONTHLYDesc=Stripe+Price+ID+for+monthly+plan&STRIPE_PRICE_YEARLYDesc=Stripe+Price+ID+for+yearly+plan)

### Or Manually:

1. **Go to**: https://railway.app/new
2. **Click**: "Deploy from GitHub repo"
3. **Select**: `idiosynsatiable/insight-atlas-production`
4. **Set Root Directory**: `backend`
5. **Add PostgreSQL**: Click "+ New" → "Database" → "PostgreSQL"

### Environment Variables to Add:

```bash
# Generate JWT Secret (run this in terminal):
openssl rand -hex 32

# Then add these in Railway:
JWT_SECRET=<paste-output-from-above>
DEMO_MODE=false
CORS_ORIGINS=https://insight-atlas-production.vercel.app
APP_BASE_URL=https://insight-atlas-production.vercel.app
STRIPE_SECRET_KEY=sk_test_51xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
STRIPE_PRICE_PRO_MONTHLY=price_xxxxx
STRIPE_PRICE_YEARLY=price_xxxxx
OPENAI_API_KEY=sk-xxxxx
OPENAI_MODEL=gpt-4.1-mini
OPENAI_POLISH_ENABLED=true
RATE_LIMIT_RPM=60
```

**Note**: Railway auto-provides `DATABASE_URL` and `PORT`

---

## Step 2: Deploy Frontend to Vercel (1 minute)

### Click This Button:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/idiosynsatiable/insight-atlas-production&project-name=insight-atlas&root-directory=frontend&env=NEXT_PUBLIC_API_BASE&envDescription=Backend+API+URL+from+Railway&envLink=https://github.com/idiosynsatiable/insight-atlas-production)

### Or Manually:

1. **Go to**: https://vercel.com/new
2. **Import**: `idiosynsatiable/insight-atlas-production`
3. **Root Directory**: `frontend`
4. **Environment Variable**:
   ```
   NEXT_PUBLIC_API_BASE=https://your-railway-url.railway.app
   ```
5. **Click**: "Deploy"

---

## Step 3: Get Stripe API Keys (3 minutes)

### Test Mode (Start Here):

1. **Go to**: https://dashboard.stripe.com/test/apikeys
2. **Copy**: "Secret key" (starts with `sk_test_`)
3. **Paste into Railway**: `STRIPE_SECRET_KEY`

### Create Products:

1. **Go to**: https://dashboard.stripe.com/test/products
2. **Click**: "Add product"

**Product 1: Pro Monthly**
- Name: `Insight Atlas Pro Monthly`
- Price: `$19.00 USD` recurring monthly
- Copy the **Price ID** (starts with `price_`)
- Paste into Railway: `STRIPE_PRICE_PRO_MONTHLY`

**Product 2: Pro Yearly**
- Name: `Insight Atlas Pro Yearly`
- Price: `$190.00 USD` recurring yearly
- Copy the **Price ID**
- Paste into Railway: `STRIPE_PRICE_YEARLY`

### Configure Webhook:

1. **Go to**: https://dashboard.stripe.com/test/webhooks
2. **Click**: "Add endpoint"
3. **Endpoint URL**: `https://your-railway-url.railway.app/stripe/webhook`
4. **Select events**:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. **Copy**: "Signing secret" (starts with `whsec_`)
6. **Paste into Railway**: `STRIPE_WEBHOOK_SECRET`

---

## Step 4: Update CORS (1 minute)

After Vercel deploys, you'll get a URL like: `https://insight-atlas-production.vercel.app`

1. **Go to Railway** → Your project → Variables
2. **Update**:
   ```
   CORS_ORIGINS=https://insight-atlas-production.vercel.app
   APP_BASE_URL=https://insight-atlas-production.vercel.app
   ```
3. Railway will auto-redeploy

---

## Step 5: Test Everything (5 minutes)

### Test Backend:
```bash
curl https://your-railway-url.railway.app/healthz
# Expected: {"status":"ok"}
```

### Test Frontend:
1. Visit: `https://insight-atlas-production.vercel.app`
2. Click "Get Started Free"
3. Register account
4. Go to "Billing"
5. Click "Upgrade to Pro Monthly"
6. Use test card: `4242 4242 4242 4242`
7. Complete checkout
8. Verify plan upgraded

### Check Webhook:
1. Go to Railway logs
2. Look for: `"Webhook received: checkout.session.completed"`
3. Verify: `"Subscription updated for user..."`

---

## 🎉 You're Live!

**Frontend**: https://insight-atlas-production.vercel.app  
**Backend**: https://your-railway-url.railway.app  
**API Docs**: https://your-railway-url.railway.app/docs

---

## 🔄 Go to Production (Later)

When ready to accept real payments:

1. **Stripe**: Switch to Live Mode
2. **Create live products** (same as test)
3. **Get live API keys** (`sk_live_...`)
4. **Configure live webhook**
5. **Update Railway** with live keys
6. **Test with real card** (start with $0.50 test)

---

## 🆘 Troubleshooting

### Backend won't start
- Check Railway logs
- Verify `DATABASE_URL` exists (auto-added by PostgreSQL)
- Ensure all environment variables are set

### CORS error
- Verify `CORS_ORIGINS` matches Vercel URL exactly
- No trailing slash
- Redeploy backend

### Stripe webhook not firing
- Check webhook URL is correct
- Verify events are selected
- Test with Stripe CLI: `stripe trigger checkout.session.completed`

---

## 📚 Full Documentation

- **Deployment**: `LIVE_DEPLOYMENT_GUIDE.md`
- **SEO**: `SEO_STRATEGY.md`
- **Security**: `SECURITY.md`
- **API**: `API.md`
- **Troubleshooting**: `RUNBOOK.md`

---

**Need Help?** Open an issue on GitHub or check the docs above.
