# Railway Port Configuration

## Target Port Setting

When Railway asks for **"Target port"** or **"Port your app is listening on"**:

### Option 1: Leave it Blank/Auto (Recommended)
- Railway will automatically detect the port from the PORT environment variable
- Your app uses `os.environ.get('PORT')` which Railway sets automatically
- **Just leave it blank or set to "auto"**

### Option 2: Use Environment Variable Reference
- If Railway requires a number, you can reference the PORT variable
- Some Railway interfaces allow: `${PORT}` or `$PORT`
- But usually leaving it blank works best

### Option 3: If You Must Enter a Number
- Enter: `5001` (this is just a fallback, Railway will override with actual PORT)
- Your app code: `PORT = int(os.environ.get('PORT', 5001))`
- Railway will set PORT to its assigned port (usually 3000, 5000, or random)

## How It Works

1. Railway assigns a port (e.g., 3000, 5000, or random)
2. Railway sets `PORT` environment variable to that port
3. Your app reads: `PORT = int(os.environ.get('PORT', 5001))`
4. App binds to `0.0.0.0:PORT` (whatever Railway assigned)
5. Railway routes traffic to that port

## Recommended Setting

**For Railway "Target port" field:**
- **Leave it blank** or select **"Auto"** or **"Detect automatically"**
- Railway will automatically use the PORT environment variable

## Verification

After deployment, check Railway logs for:
```
Starting server on 0.0.0.0:XXXX
```
Where XXXX is the port Railway assigned (should match Railway's PORT env var).
