# SendGrid Setup Guide

## Why SendGrid?

Railway (and most cloud platforms) **block outbound SMTP connections on port 587** to prevent spam. This is why Gmail SMTP was timing out.

SendGrid uses HTTP API instead of SMTP, which works perfectly on Railway!

## Setup Steps

### 1. Create Free SendGrid Account

1. Go to [https://sendgrid.com/](https://sendgrid.com/)
2. Click "Start for Free"
3. Sign up with your email
4. **Free tier includes: 100 emails/day** (perfect for your needs!)

### 2. Verify Your Sender Email

1. In SendGrid dashboard, go to **Settings → Sender Authentication**
2. Click **"Verify a Single Sender"**
3. Fill in your details:
   - From Email: `imajumd1@gmail.com`
   - From Name: `Anya AI News Agent`
4. Check your email and click the verification link

### 3. Create API Key

1. Go to **Settings → API Keys**
2. Click **"Create API Key"**
3. Name: `Railway Email Service`
4. Permissions: **"Full Access"** (or at minimum "Mail Send")
5. Click **"Create & View"**
6. **IMPORTANT**: Copy the API key now (it won't be shown again!)
   - It looks like: `SG.xxxxxxxxxxxx...`

### 4. Add to Railway Environment Variables

1. Go to your Railway project dashboard
2. Click on your service
3. Go to **"Variables"** tab
4. Click **"+ New Variable"**
5. Add:
   ```
   Variable: SENDGRID_API_KEY
   Value: SG.xxxxxxxxxxxx... (paste your key)
   ```
6. Click **"Add"**
7. Railway will automatically redeploy

### 5. Test Email

After Railway redeploys (1-2 minutes):
1. Fetch some news on your app
2. Enter an email address
3. Click "Send Email"
4. Should work instantly! ⚡

## How It Works

**Before (SMTP - Blocked):**
```
Your App → Port 587 → Gmail SMTP ❌ (Blocked by Railway)
```

**After (SendGrid API - Works!):**
```
Your App → HTTPS API → SendGrid → Recipient ✅
```

## Troubleshooting

**"SendGrid API error"**
- Check API key is correct
- Make sure sender email is verified
- Check SendGrid dashboard for blocked sends

**Still getting "Email service not configured"**
- Make sure you added `SENDGRID_API_KEY` to Railway
- Check Railway redeployed after adding variable
- Variable name must be exactly: `SENDGRID_API_KEY`

## Benefits

✅ No SMTP port blocking issues
✅ Faster email delivery
✅ Better deliverability 
✅ Email analytics in SendGrid dashboard
✅ 100 free emails/day
✅ Works on all cloud platforms
