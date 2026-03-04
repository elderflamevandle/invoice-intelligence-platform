from fastapi import FastAPI
from pydantic import BaseModel

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag
import uvicorn
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from config import API_HOST, API_PORT
from logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Vendor Invoice Intelligence API",
    description="API for Freight Cost Prediction & Invoice Risk Flagging"
)

class FreightRequest(BaseModel):
    Dollars: float

class FreightResponse(BaseModel):
    Predicted_Freight: float

class InvoiceFlagRequest(BaseModel):
    invoice_quantity: float
    invoice_dollars: float
    Freight: float
    total_item_quantity: float
    total_item_dollars: float

class InvoiceFlagResponse(BaseModel):
    Predicted_Flag: float
    Requires_Manual_Approval: bool

@app.post("/predict_freight", response_model=FreightResponse)
def predict_freight(request: FreightRequest):
    logger.info(f"Received freight prediction request for Dollars: {request.Dollars}")
    input_data = {"Dollars": [request.Dollars]}
    df = predict_freight_cost(input_data)
    prediction = df["Predicted_Freight"][0]
    return FreightResponse(Predicted_Freight=prediction)

@app.post("/predict_invoice_flag", response_model=InvoiceFlagResponse)
def predict_flag(request: InvoiceFlagRequest):
    logger.info(f"Received anomaly risk prediction check for PO quantity: {request.total_item_quantity}")
    input_data = {
        "invoice_quantity": [request.invoice_quantity],
        "invoice_dollars": [request.invoice_dollars],
        "Freight": [request.Freight],
        "total_item_quantity": [request.total_item_quantity],
        "total_item_dollars": [request.total_item_dollars]
    }
    df = predict_invoice_flag(input_data)
    prediction = df["Predicted_Flag"][0]
    return InvoiceFlagResponse(
        Predicted_Flag=prediction,
        Requires_Manual_Approval=bool(prediction)
    )

if __name__ == "__main__":
    logger.info(f"Starting API Server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
