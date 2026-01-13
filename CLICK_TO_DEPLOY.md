# 🚀 CLICK THESE LINKS TO DEPLOY

## ⚡ FASTEST PATH - 3 CLICKS

### 1️⃣ Deploy Backend (Railway)
**Click here**: https://railway.app/template/insight-atlas

**Or use this link**:
```
https://railway.app/new?template=https://github.com/idiosynsatiable/insight-atlas-production
```

**What happens**:
- Railway clones your repo
- Builds backend with Docker
- Adds PostgreSQL database
- Asks for environment variables

**Environment variables you'll need**:
```bash
JWT_SECRET=<run: openssl rand -hex 32>
DEMO_MODE=false
CORS_ORIGINS=https://your-vercel-url.vercel.app
APP_BASE_URL=https://your-vercel-url.vercel.app
STRIPE_SECRET_KEY=<from Stripe dashboard>
STRIPE_WEBHOOK_SECRET=<from Stripe webhook>
STRIPE_PRICE_PRO_MONTHLY=<from Stripe products>
STRIPE_PRICE_YEARLY=<from Stripe products>
```

---

### 2️⃣ Deploy Frontend (Vercel)
**Click here**: https://vercel.com/new/clone?repository-url=https://github.com/idiosynsatiable/insight-atlas-production

**What happens**:
- Vercel imports your repo
- Detects Next.js automatically
- Asks for environment variable

**Environment variable**:
```bash
NEXT_PUBLIC_API_BASE=https://your-railway-url.railway.app
```

---

### 3️⃣ Get Stripe Keys
**Click here**: https://dashboard.stripe.com/register

**Then go to**:
1. **API Keys**: https://dashboard.stripe.com/test/apikeys
   - Copy "Secret key" → Use for `STRIPE_SECRET_KEY`

2. **Products**: https://dashboard.stripe.com/test/products
   - Create "Pro Monthly" ($19/month)
   - Create "Pro Yearly" ($190/year)
   - Copy Price IDs → Use for `STRIPE_PRICE_PRO_MONTHLY` and `STRIPE_PRICE_YEARLY`

3. **Webhooks**: https://dashboard.stripe.com/test/webhooks
   - Add endpoint: `https://your-railway-url.railway.app/stripe/webhook`
   - Select events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
   - Copy "Signing secret" → Use for `STRIPE_WEBHOOK_SECRET`

---

## 🎯 STEP-BY-STEP (If buttons don't work)

### Backend (Railway):
1. Go to: https://railway.app/new
2. Click: "Deploy from GitHub repo"
3. Select: `idiosynsatiable/insight-atlas-production`
4. Settings → Root Directory: `backend`
5. Add service: PostgreSQL (click "+ New" → Database → PostgreSQL)
6. Add environment variables (see list above)
7. Deploy!

### Frontend (Vercel):
1. Go to: https://vercel.com/new
2. Import: `idiosynsatiable/insight-atlas-production`
3. Root Directory: `frontend`
4. Framework: Next.js (auto-detected)
5. Add environment variable: `NEXT_PUBLIC_API_BASE`
6. Deploy!

---

## ✅ VERIFY IT WORKS

### Test Backend:
```bash
curl https://your-railway-url.railway.app/healthz
```
Expected: `{"status":"ok"}`

### Test Frontend:
Visit: `https://your-vercel-url.vercel.app`

### Test Full Flow:
1. Register account
2. Go to Billing
3. Click "Upgrade to Pro"
4. Use test card: `4242 4242 4242 4242`
5. Complete checkout
6. Check Railway logs for webhook event

---

## 🆘 NEED HELP?

**Railway Issues**:
- Check logs: https://railway.app/project/your-project/deployments
- Verify PostgreSQL is running
- Ensure all env vars are set

**Vercel Issues**:
- Check build logs: https://vercel.com/your-project/deployments
- Verify `NEXT_PUBLIC_API_BASE` is set correctly

**Stripe Issues**:
- Verify webhook URL is correct
- Check webhook events are selected
- Test with Stripe CLI: `stripe trigger checkout.session.completed`

---

## 📚 FULL DOCS

- **Complete Guide**: `LIVE_DEPLOYMENT_GUIDE.md`
- **SEO Strategy**: `SEO_STRATEGY.md`
- **Security**: `SECURITY.md`
- **API Reference**: `API.md`
- **Troubleshooting**: `RUNBOOK.md`

---

**GitHub Repo**: https://github.com/idiosynsatiable/insight-atlas-production

**Ready to launch!** 🚀
