from flask import Flask, request, jsonify, render_template
import os
import logging
from datetime import datetime
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from cnnClassifier.utils.common import decodeImage
from cnnClassifier.pipeline.prediction import PredictionPipeline

# Load environment variables
load_dotenv()

# Set encoding
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
log_file = os.getenv('LOG_FILE', 'logs/app.log')
os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)

logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
CORS(app, resources={r"/api/*": {"origins": cors_origins}})


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        try:
            self.classifier = PredictionPipeline(self.filename)
            logger.info("PredictionPipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PredictionPipeline: {str(e)}")
            raise


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error loading home page: {str(e)}")
        return jsonify({"error": "Failed to load home page"}), 500


@app.route("/health", methods=['GET'])
@cross_origin()
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200


@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRoute():
    """Training endpoint - disabled in production by default"""
    try:
        if os.getenv('TRAINING_ENABLED', 'False').lower() != 'true':
            logger.warning("Training endpoint called but TRAINING_ENABLED is False")
            return jsonify({"error": "Training is disabled in this environment"}), 403
        
        logger.info("Starting training pipeline")
        result = os.system("python main.py")
        
        if result == 0:
            logger.info("Training completed successfully")
            return jsonify({"status": "success", "message": "Training completed"}), 200
        else:
            logger.error(f"Training failed with exit code {result}")
            return jsonify({"error": "Training failed"}), 500
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    """Prediction endpoint"""
    try:
        if 'image' not in request.json:
            logger.warning("Predict request missing image data")
            return jsonify({"error": "Image data required"}), 400
        
        image = request.json['image']
        decodeImage(image, clApp.filename)
        result = clApp.classifier.predict()
        
        logger.info(f"Prediction completed: {result}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    try:
        clApp = ClientApp()
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 8080))
        debug = os.getenv('FLASK_ENV', 'production') == 'development'
        
        logger.info(f"Starting Flask app on {host}:{port}")
        app.run(host=host, port=port, debug=debug, threaded=True)
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}")
        raise

    app.run(host='0.0.0.0', port=8080) #for AWS

