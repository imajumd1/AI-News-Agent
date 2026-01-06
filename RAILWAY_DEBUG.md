# Railway Deployment Debugging Guide

## Common Issues and Solutions

### 1. "Application failed to respond" Error

**Causes:**
- App not binding to `0.0.0.0` (must use Railway's PORT env var)
- Missing Procfile
- Environment variables not set
- App crashing on startup

**Solutions:**

#### Check Railway Logs
1. Go to your Railway project dashboard
2. Click on your service
3. Click "Deployments" tab
4. Click on the latest deployment
5. Check "Build Logs" and "Deploy Logs"

#### Verify Configuration
- ✅ **Procfile exists** - Should contain: `web: python3 app.py`
- ✅ **Port configuration** - App should use `os.environ.get('PORT', 5001)`
- ✅ **Host binding** - App should bind to `0.0.0.0`, not `127.0.0.1`
- ✅ **Environment variables** - Set `OPENAI_API_KEY` in Railway dashboard

### 2. Environment Variables

**Required Variables:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `PORT` - Automatically set by Railway (don't set manually)
- `FLASK_DEBUG` - Set to `False` for production

**How to Set:**
1. Go to Railway project dashboard
2. Click on your service
3. Click "Variables" tab
4. Add `OPENAI_API_KEY` with your key value
5. Add `FLASK_DEBUG` = `False`

### 3. Build Failures

**Check:**
- `requirements.txt` exists and is correct
- Python version is compatible (3.9+)
- All dependencies are listed

### 4. Runtime Errors

**Common Issues:**
- Missing imports
- File path issues (use relative paths)
- Database/connection issues

**Debug Steps:**
1. Check deploy logs for Python tracebacks
2. Test locally with same environment variables
3. Add print statements for debugging

## Quick Fix Checklist

- [ ] Procfile exists with `web: python3 app.py`
- [ ] App uses `os.environ.get('PORT')` for port
- [ ] App binds to `0.0.0.0` not `127.0.0.1`
- [ ] `OPENAI_API_KEY` is set in Railway variables
- [ ] `requirements.txt` includes all dependencies
- [ ] No hardcoded paths or local file references
- [ ] Check Railway deploy logs for specific errors

## Testing Locally with Railway Environment

```bash
# Set Railway-like environment
export PORT=5001
export FLASK_DEBUG=False
export OPENAI_API_KEY=your_key_here

# Run the app
python3 app.py
```

## Railway CLI Commands

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Set variables
railway variables set OPENAI_API_KEY=your_key
```
