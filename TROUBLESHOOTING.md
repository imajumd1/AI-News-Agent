# Troubleshooting Guide

## Server Not Running

### Check if server is running:
```bash
lsof -ti:5001
```

If nothing is returned, start the server:
```bash
cd ~/ai_news_agent
python3 app.py
```

### Check server logs:
The server runs in the terminal where you started it. Look for:
- `Starting server on http://localhost:5001`
- Any error messages

## Agent Not Working

### 1. Check Browser Console
- Open browser Developer Tools (F12 or Cmd+Option+I)
- Go to Console tab
- Look for JavaScript errors
- Try clicking "Fetch Latest News" and watch for errors

### 2. Test the API Directly
```bash
curl -X POST http://localhost:5001/run \
  -H "Content-Type: application/json" \
  -d '{"days": 3, "mode": "fast", "fetchContent": false}'
```

This should return JSON with articles. If it works, the issue is in the frontend.

### 3. Check Network Tab
- Open Developer Tools → Network tab
- Click "Fetch Latest News"
- Look for the `/run` request
- Check if it's pending (waiting - scraping takes 40-60 seconds)
- Check the response status code

### 4. Common Issues

**Issue: Request times out**
- **Solution**: Scraping 31 sources takes 40-60 seconds. This is normal. Wait for it to complete.

**Issue: CORS errors**
- **Solution**: Make sure you're accessing `http://localhost:5001` (not a different port)

**Issue: "Cannot connect"**
- **Solution**: 
  1. Check if server is running: `lsof -ti:5001`
  2. Restart server: `python3 app.py`
  3. Try a different browser

**Issue: No articles found**
- **Solution**: 
  - Try increasing "Days to look back" to 14 or 30
  - Some RSS feeds may be temporarily unavailable
  - Check server terminal for error messages

## Quick Fixes

### Restart Server:
```bash
# Kill existing server
lsof -ti:5001 | xargs kill

# Start fresh
cd ~/ai_news_agent
python3 app.py
```

### Clear Browser Cache:
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
- Or clear browser cache completely

### Check Dependencies:
```bash
cd ~/ai_news_agent
pip3 install -r requirements.txt
```

## Still Not Working?

1. Check the server terminal for error messages
2. Open browser console (F12) and check for JavaScript errors
3. Verify all dependencies are installed
4. Try accessing `http://127.0.0.1:5001` instead of `localhost:5001`
