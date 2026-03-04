import joblib
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DB_PATH, MODEL_DIR, FREIGHT_MODEL_PATH
from logger import get_logger

logger = get_logger(__name__)

from data_preprocessing import load_vendor_invoice_data, prepare_features, split_data
from modeling_evaluation import (
    train_linear_regression,
    train_decision_tree,
    train_random_forest,
    evaluate_model
)

def main():
    MODEL_DIR.mkdir(exist_ok=True)
    logger.info("Starting Freight Cost Prediction Training Pipeline...")

    # Load data
    df = load_vendor_invoice_data(DB_PATH)

    # Prepare data
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Train models
    lr_model = train_linear_regression(X_train, y_train)
    dt_model = train_decision_tree(X_train, y_train)
    rf_model = train_random_forest(X_train, y_train)

    # Evaluate models
    results = []
    results.append(evaluate_model(lr_model, X_test, y_test, "Linear Regression"))
    results.append(evaluate_model(dt_model, X_test, y_test, "Decision Tree Regression"))
    results.append(evaluate_model(rf_model, X_test, y_test, "Random Forest Regression"))

    # Select best model (lowest MAE)
    best_model_info = min(results, key=lambda x: x["mae"])
    best_model_name = best_model_info["model_name"]

    best_model = {
        "Linear Regression": lr_model,
        "Decision Tree Regression": dt_model,
        "Random Forest Regression": rf_model
    }[best_model_name]

    # Save best model
    joblib.dump(best_model, FREIGHT_MODEL_PATH)
    logger.info(f"Best model saved: {best_model_name}")
    logger.info(f"Model path: {FREIGHT_MODEL_PATH}")


if __name__ == "__main__":
    main()
