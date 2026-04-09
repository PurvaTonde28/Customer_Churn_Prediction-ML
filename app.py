from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import os

# --------------------------------------------------
# App Initialization
# --------------------------------------------------
app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predicts customer churn using a trained ML pipeline",
    version="1.0"
)

# --------------------------------------------------
# Load Model & Threshold (SAFE PATH HANDLING)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "churn_pipeline.pkl"))
threshold = joblib.load(os.path.join(BASE_DIR, "threshold.pkl"))

# --------------------------------------------------
# Pydantic Input Schema (STRICT VALIDATION)
# --------------------------------------------------
class CustomerInput(BaseModel):
    tenure: int = Field(..., ge=0, le=72)
    MonthlyCharges: float = Field(..., ge=0)
    TotalCharges: float = Field(..., ge=0)

    avg_monthly_spend: float = Field(..., ge=0)
    service_count: int = Field(..., ge=0, le=5)

    contract_risk: int = Field(..., ge=0, le=1)
    payment_risk: int = Field(..., ge=0, le=1)

    gender: str
    SeniorCitizen: int = Field(..., ge=0, le=1)
    Partner: str
    Dependents: str
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str

    class Config:
        schema_extra = {
            "example": {
                "tenure": 12,
                "MonthlyCharges": 85.5,
                "TotalCharges": 1020.0,
                "avg_monthly_spend": 85.0,
                "service_count": 2,
                "contract_risk": 1,
                "payment_risk": 1,
                "gender": "Male",
                "SeniorCitizen": 0,
                "Partner": "Yes",
                "Dependents": "No",
                "PhoneService": "Yes",
                "MultipleLines": "No",
                "InternetService": "Fiber optic",
                "OnlineSecurity": "No",
                "OnlineBackup": "Yes",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "Yes",
                "StreamingMovies": "No",
                "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check"
            }
        }

# --------------------------------------------------
# Health Check Endpoint
# --------------------------------------------------
@app.get("/")
def health_check():
    return {"status": "Customer Churn Prediction API is running"}

# --------------------------------------------------
# Prediction Endpoint
# --------------------------------------------------
@app.post("/predict")
def predict_churn(customer: CustomerInput):
    """
    Predicts churn probability and risk label for a single customer
    """

    # Convert validated input to DataFrame
    input_df = pd.DataFrame([customer.dict()])

    # Predict churn probability
    churn_probability = model.predict_proba(input_df)[0][1]

    # Apply optimized threshold
    churn_prediction = int(churn_probability >= threshold)

    return {
        "churn_probability": round(churn_probability, 4),
        "churn_prediction": churn_prediction,
        "risk_label": "High Risk" if churn_prediction else "Low Risk"
    }
