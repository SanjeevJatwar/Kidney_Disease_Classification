# Deploy to Hugging Face Spaces (Docker)

## Why Docker SDK?

- **Full control** over environment and dependencies
- **Production-ready** Flask app with existing UI
- **16GB RAM** vs Render's 512MB (TensorFlow compatible)
- **Always-on** - No cold starts
- **Port 7860** - HF Spaces standard

## Quick Deploy

### Prerequisites
```powershell
# Login to Hugging Face (token from https://huggingface.co/settings/tokens)
huggingface-cli login
```

### Option 1: CLI Deployment (Recommended)

1. **Create Docker Space**
```powershell
cd "D:\world of ml\Kidney_Disease_Classification"
huggingface-cli repo create kidney-disease-classifier --type space --space_sdk docker
```

2. **Clone & Copy Files**
```powershell
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/kidney-disease-classifier
cd kidney-disease-classifier

# Copy all files
Copy-Item ..\Dockerfile.huggingface .\Dockerfile
Copy-Item ..\app.py .
Copy-Item ..\requirements.txt .
Copy-Item ..\setup.py .
Copy-Item -Recurse ..\src .
Copy-Item -Recurse ..\config .
Copy-Item -Recurse ..\templates .
Copy-Item -Recurse ..\artifacts .
Copy-Item ..\README.md .\README.md

# Create HF Spaces README
@"
---
title: Kidney Disease Classification
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Kidney Disease Classifier

Deep learning model (VGG16) for kidney CT scan classification.

**Categories**: Cyst, Tumor, Stone, Normal

Upload a CT scan image to get instant classification with confidence scores.
"@ | Out-File -FilePath "README.md" -Encoding utf8
```

3. **Push to HF**
```powershell
git lfs install
git lfs track "*.h5"
git add .gitattributes
git add .
git commit -m "Deploy Flask app with Docker"
git push
```

4. **Wait for Build**: HF builds Docker image (~5-7 minutes)

5. **Access Your App**: 
```
https://huggingface.co/spaces/YOUR_USERNAME/kidney-disease-classifier
```

### Option 2: Web UI

1. **Create Space**: https://huggingface.co/new-space
   - Name: `kidney-disease-classifier`
   - SDK: **Docker**
   - Click "Create Space"

2. **Upload Files**:
   - Rename `Dockerfile.huggingface` → `Dockerfile`
   - Upload: `Dockerfile`, `app.py`, `requirements.txt`, `setup.py`, `README.md`
   - Upload folders: `src/`, `config/`, `templates/`, `artifacts/`

3. **HF Auto-builds** and deploys

## Comparison: Gradio vs Docker

| Feature | Gradio SDK | Docker SDK |
|---------|-----------|-----------|
| **Setup** | Simple (1 file) | Complex (Dockerfile) |
| **UI** | Auto-generated | Custom (templates/index.html) |
| **Flexibility** | Limited | Full control |
| **Build Time** | 2-3 min | 5-7 min |
| **Best For** | Quick demos | Production apps |

You chose Docker for full control over the Flask app and custom HTML interface! 🚀
- Upload via:
  - Git LFS: `git lfs install && git lfs track "*.h5"`
  - Web UI: Direct file upload
  - Google Drive link in description

## Free Tier Limits

- **CPU Basic**: 2 CPU cores, 16GB RAM
- **Storage**: 50GB
- **Always on**: Yes (unlike Render free tier)
- **No spin-down**: Better than Render free tier!

## Why Hugging Face?

✅ Better for ML models than Render free tier
✅ No memory issues (16GB vs 512MB)
✅ Persistent storage
✅ No sleep/wake delays
✅ Built-in ML community discovery
✅ Free GPU available (with approval)

## Example Space

Check out: https://huggingface.co/spaces/gradio/image-classification
