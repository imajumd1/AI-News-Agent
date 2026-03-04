# Railway Deployment Guide

## Quick Setup

Your AI News Agent is configured for automatic deployment via Railway.

### Required Environment Variables

Set these in your Railway project dashboard (Settings → Variables):

#### Essential Variables

```bash
# OpenAI API Key (Required for Full Mode with AI summaries)
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Email Configuration (Optional - for email feature)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password_here
MAIL_FROM=your_email@gmail.com
```

### Deployment Process

1. **Connect GitHub**: Your Railway project is already connected to your GitHub repository
2. **Set Environment Variables**: Add the variables above in Railway dashboard
3. **Deploy**: Push to `main` branch - Railway will automatically deploy

### Verify Deployment

1. Check Railway deployment logs for:
   ```
   🚀 AI News Agent - Web Server
   Starting server on 0.0.0.0:$PORT
   ```

2. Visit your Railway app URL
3. Test the health check endpoint: `https://your-app.railway.app/health`

### Troubleshooting

#### Application Failed to Respond

**Common Causes:**
- Missing `OPENAI_API_KEY` environment variable
- Build failed (check Railway logs)
- Port binding issues (should use Railway's `$PORT` variable)

**Solutions:**
1. Check Railway dashboard → Deployments → View Logs
2. Verify all environment variables are set correctly
3. Ensure `OPENAI_API_KEY` is valid and starts with `sk-`

#### Fast Mode vs Full Mode

- **Fast Mode**: Uses RSS feed summaries (no API key required)
- **Full Mode**: Uses AI-generated summaries (requires `OPENAI_API_KEY`)

If `OPENAI_API_KEY` is not set, the app will still work but only in Fast Mode.

### Configuration Files

- `railway.json` - Railway build and deploy configuration
- `Procfile` - Alternative process configuration
- `runtime.txt` - Python version specification
- `requirements.txt` - Python dependencies

### Health Check

Railway uses the `/health` endpoint to verify the application is running:

```bash
curl https://your-app.railway.app/health
# Response: {"status": "healthy", "service": "AI News Agent"}
```

### Manual Redeployment

If needed, trigger a manual redeployment in Railway dashboard:
1. Go to your project
2. Click on the service
3. Click "Redeploy" button

### Support

For Railway-specific issues, refer to:
- [Railway Docs](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)

For application issues, check the repository README.md
