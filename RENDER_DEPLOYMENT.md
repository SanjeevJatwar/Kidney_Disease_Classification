# Deploy to Render

## Quick Deploy Steps

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up/login (can use GitHub)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`
   - Click "Apply"
   - Wait 5-10 minutes for build

3. **Your app will be live at:**
   ```
   https://kidney-disease-classifier.onrender.com
   ```

## Important Notes

- **Free tier limitations:**
  - Spins down after 15 minutes of inactivity
  - First request after idle takes ~30 seconds to wake up
  - 512MB RAM, 0.1 CPU

- **Model file:** Make sure `artifacts/training/model.h5` exists before deployment

- **Port:** Render uses port 10000 (already configured)

## Upgrade to Paid Plan

For production (no spin-down):
- Starter: $7/month
- Standard: $25/month

## Alternative: Render Free Docker

If Blueprint doesn't work:
1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect GitHub repo
4. Settings:
   - **Name:** kidney-disease-classifier
   - **Environment:** Docker
   - **Region:** Singapore (or closest to you)
   - **Branch:** main
   - **Plan:** Free
   - **Health Check Path:** /health
5. Click "Create Web Service"

## Monitor Deployment

View logs in Render dashboard to track:
- Docker build progress
- TensorFlow installation
- App startup
- Health check status

Your app is production-ready with Docker!
