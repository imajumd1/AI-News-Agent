# Railway Redeploy Instructions

## ✅ Changes Pushed to GitHub

The Railway deployment fixes have been pushed to:
- Repository: https://github.com/imajumd1/AI-News-Agent
- Latest commit: `e5902ee` - "Fix Railway deployment configuration"

## Automatic Deployment

If your Railway project is connected to GitHub, it should **automatically redeploy** when it detects the new commit.

**Check deployment status:**
1. Go to https://railway.app
2. Open your project
3. Check the "Deployments" tab
4. You should see a new deployment in progress or completed

## Manual Redeploy (if needed)

### Option 1: Via Railway Dashboard
1. Go to your Railway project dashboard
2. Click on your service
3. Click the "..." menu (three dots)
4. Select "Redeploy"

### Option 2: Via Railway CLI
```bash
# Install Railway CLI (if not installed)
npm i -g @railway/cli

# Login
railway login

# Link to your project (if not already linked)
railway link

# Trigger redeploy
railway up
```

### Option 3: Force Redeploy from GitHub
1. Go to Railway dashboard
2. Settings → Source
3. Click "Redeploy" or disconnect/reconnect GitHub

## Verify Deployment

After redeploy, check:

1. **Deploy Logs:**
   - Railway dashboard → Your service → Deployments → Latest deployment → Deploy Logs
   - Look for: "Starting server on 0.0.0.0:XXXX"

2. **Environment Variables:**
   - Railway dashboard → Your service → Variables
   - Ensure `OPENAI_API_KEY` is set
   - Ensure `FLASK_DEBUG=False` (for production)

3. **Test the App:**
   - Visit your Railway app URL
   - Should see the AI News Agent interface
   - Try clicking "Fetch Latest News"

## Troubleshooting

If the app still fails:

1. **Check Build Logs:**
   - Look for Python import errors
   - Check if all dependencies installed correctly

2. **Check Deploy Logs:**
   - Look for "Application failed to respond" errors
   - Check if port binding is correct
   - Verify the app started successfully

3. **Common Issues:**
   - Missing `OPENAI_API_KEY` → Set in Railway Variables
   - Port binding error → Should be fixed now (uses Railway PORT)
   - Import errors → Check requirements.txt

## What Was Fixed

✅ App now uses Railway's PORT environment variable
✅ App binds to 0.0.0.0 (required for Railway)
✅ Procfile added for Railway deployment
✅ railway.json configuration added
✅ Debug mode respects FLASK_DEBUG environment variable
