from data_preprocessing import load_invoice_data, split_data, scale_features, apply_labels
from modeling_evaluation import train_random_forest, evaluate_classifier
import joblib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import SCALER_PATH, FLAG_MODEL_PATH
from logger import get_logger

logger = get_logger(__name__)

FEATURES = [
    "invoice_quantity",
    "invoice_dollars",
    "Freight",
    "total_item_quantity",
    "total_item_dollars"
]

TARGET = "flag_invoice"
    
    
def main():
    logger.info("Starting Invoice Risk Flagging Training Pipeline...")
    # Load data
    df = load_invoice_data()
    df = apply_labels(df)

    # Prepare data
    X_train, X_test, y_train, y_test = split_data(df, FEATURES, TARGET)
    X_train_scaled, X_test_scaled = scale_features(
        X_train, X_test, SCALER_PATH
    )
    
    # Train and evaluate models
    grid_search = train_random_forest(X_train_scaled, y_train)

    evaluate_classifier(
        grid_search.best_estimator_,
        X_test_scaled,
        y_test,
        "Random Forest Classifier"
    )
    
    # Save best model
    joblib.dump(grid_search.best_estimator_, FLAG_MODEL_PATH)
    logger.info(f"Best model saved: {FLAG_MODEL_PATH}")

if __name__ == "__main__":
    main()
