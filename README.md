# 🩺 Kidney Disease Classification

Deep learning-based CT scan classifier for kidney disease detection using CNN and VGG16 transfer learning.

## 📌 Overview

End-to-end machine learning project that classifies kidney CT scans into 4 categories:
- **Cyst** - Fluid-filled sacs in the kidney
- **Tumor** - Abnormal tissue growth
- **Stone** - Kidney stones
- **Normal** - Healthy kidney tissue

## ✨ Features

- VGG16 transfer learning with TensorFlow 2.12
- Production-ready Flask API with health checks
- Docker containerization for easy deployment
- MLflow experiment tracking
- DVC data pipeline
- CORS-enabled REST API

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/SanjeevJatwar/Kidney_Disease_Classification.git
cd Kidney_Disease_Classification

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run training pipeline
python main.py

# Start Flask app
python app.py
```

Access at: http://localhost:8080

### 4. Run Locally
```bash

Access at: http://localhost:8080

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# Check health
curl http://localhost:8080/health

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## ☁️ Deploy to Render (Free)

1. Push to GitHub: `git push origin main`
2. Go to [render.com](https://render.com) → New+ → Blueprint
3. Connect repo: `SanjeevJatwar/Kidney_Disease_Classification`
4. Render auto-detects `render.yaml`
5. Click "Apply"

**Live in ~10 minutes at:** `https://kidney-disease-classifier.onrender.com`

**Note:** Free tier spins down after 15 min idle. Upload trained model separately to Render (not in git).

## 📁 Project Structure

```
Kidney_Disease_Classification/
├── app.py                    # Flask REST API
├── main.py                   # Training pipeline
├── Dockerfile                # Container image
├── docker-compose.yml        # Multi-container orchestration
├── render.yaml               # Render deployment config
├── requirements.txt          # Python dependencies
├── setup.py                  # Package installer
├── dvc.yaml                  # DVC pipeline stages
├── params.yaml              # Model hyperparameters
├── config/
│   └── config.yaml          # App configuration
├── src/cnnClassifier/
│   ├── components/          # Data ingestion, model prep, training
│   ├── config/              # Configuration manager
│   ├── entity/              # Config entities
│   ├── pipeline/            # Training & prediction pipelines
│   └── utils/               # Common utilities
├── templates/
│   └── index.html           # Web UI
└── artifacts/               # Models & data (gitignored)
```

## 🔌 API Endpoints

### Health Check
```bash
GET /health
# Response: {"status":"healthy","timestamp":"2026-02-01T..."}
```

### Prediction
```bash
POST /predict
Content-Type: application/json


## 🔌 API Endpoints

### Health Check
```bash
GET /health
# Response: {"status":"healthy","timestamp":"2026-02-01T15:26:15.852887"}
```

### Prediction
```bash
POST /predict
Content-Type: application/json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
# Response: [{"image": "Cyst"}]
```

## 🧪 Training Pipeline

```bash
# Full pipeline
python main.py

# DVC pipeline
dvc repro

# Individual stages
python src/cnnClassifier/pipeline/stage_01_data_ingestion.py
python src/cnnClassifier/pipeline/stage_02_prepare_base_model.py
python src/cnnClassifier/pipeline/stage_03_model_training.py
python src/cnnClassifier/pipeline/stage_04_model_evaluation.py
```

## 📊 MLflow Tracking

```bash
mlflow ui
# Open http://localhost:5000
```

## 🏗️ Model Details

- **Architecture:** VGG16 (ImageNet pre-trained)
- **Input Size:** 224×224×3 RGB
- **Classes:** 4 (Cyst, Normal, Stone, Tumor)
- **Optimizer:** SGD
- **Loss:** Categorical Crossentropy

## 📦 Tech Stack

- **Backend:** Flask 2.3.3, Python 3.9
- **ML:** TensorFlow 2.12.0, Keras
- **Pipeline:** DVC 3.47.0
- **Tracking:** MLflow 2.2.2
- **Deployment:** Docker, Render

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/NewFeature`
3. Commit changes: `git commit -m 'Add NewFeature'`
4. Push: `git push origin feature/NewFeature`
5. Open Pull Request

## 📄 License

MIT License

## 👨‍💻 Author

**Sanjeev Jatwar**
- GitHub: [@SanjeevJatwar](https://github.com/SanjeevJatwar)

---

⭐ **Star this repo if you find it helpful!**
