from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

app = FastAPI(title="Customer Churn Prediction API", version="1.0")

MODEL_PATH = "models/churn_model.pkl"

class CustomerRFM(BaseModel):
    recency_days: int
    frequency: int
    total_spend: float
    avg_order_value: float
    cancelled_orders: int

@app.get("/")
def health_check():
    return {"status": "active", "service": "E-Commerce Churn Inference API"}

@app.post("/predict")
def predict_churn(customer: CustomerRFM):
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=500, detail="Model artifact not found. Run main.py first.")
    
    model = joblib.load(MODEL_PATH)
    
    features = [[
        customer.recency_days,
        customer.frequency,
        customer.total_spend,
        customer.avg_order_value,
        customer.cancelled_orders
    ]]
    
    churn_prediction = int(model.predict(features)[0])
    churn_probability = float(model.predict_proba(features)[0][1])
    
    return {
        "churn_prediction": churn_prediction,
        "churn_probability": round(churn_probability, 4),
        "risk_level": "HIGH" if churn_probability > 0.6 else "LOW"
    }