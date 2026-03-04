import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data paths
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "inventory.db"

# Model paths
MODEL_DIR = BASE_DIR / "models"
FREIGHT_MODEL_PATH = MODEL_DIR / "predict_freight_model.pkl"
FLAG_MODEL_PATH = MODEL_DIR / "predict_flag_invoice.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# For Streamlit communicating to FastAPI. Local is 127.0.0.1, Docker is "api"
API_URL = os.getenv("API_URL", f"http://127.0.0.1:{API_PORT}")

# Logging configuration
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "app.log"
