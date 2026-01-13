import streamlit as st
import requests

st.set_page_config(page_title="Customer Churn Predictor", layout="centered")

st.title("📉 Customer Churn Prediction")
st.write("Enter customer details to predict churn risk")

API_URL = "http://127.0.0.1:8000/predict"

# -----------------------------
# Input Form
# -----------------------------
with st.form("churn_form"):
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0, value=80.0)
    TotalCharges = st.number_input("Total Charges", min_value=0.0, value=1000.0)

    avg_monthly_spend = st.number_input("Average Monthly Spend", min_value=0.0, value=80.0)
    service_count = st.slider("Number of Services", 0, 5, 2)

    contract_risk = st.selectbox("Contract Type", ["Safe", "Month-to-Month"])
    payment_risk = st.selectbox("Payment Method Risk", ["Low Risk", "High Risk"])

    gender = st.selectbox("Gender", ["Male", "Female"])
    SeniorCitizen = st.selectbox("Senior Citizen", ["No", "Yes"])
    Partner = st.selectbox("Partner", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["Yes", "No"])
    PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
    MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No"])
    InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    OnlineSecurity = st.selectbox("Online Security", ["Yes", "No"])
    OnlineBackup = st.selectbox("Online Backup", ["Yes", "No"])
    DeviceProtection = st.selectbox("Device Protection", ["Yes", "No"])
    TechSupport = st.selectbox("Tech Support", ["Yes", "No"])
    StreamingTV = st.selectbox("Streaming TV", ["Yes", "No"])
    StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No"])
    Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
    PaymentMethod = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )

    submitted = st.form_submit_button("🔍 Predict Churn")

# -----------------------------
# Prediction
# -----------------------------
if submitted:
    payload = {
        "tenure": tenure,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges,
        "avg_monthly_spend": avg_monthly_spend,
        "service_count": service_count,
        "contract_risk": 1 if contract_risk == "Month-to-Month" else 0,
        "payment_risk": 1 if payment_risk == "High Risk" else 0,
        "gender": gender,
        "SeniorCitizen": 1 if SeniorCitizen == "Yes" else 0,
        "Partner": Partner,
        "Dependents": Dependents,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        st.subheader("📊 Prediction Result")

        if result["churn_prediction"] == 1:
            st.error(f"⚠️ High Risk of Churn ({result['churn_probability']:.2%})")
        else:
            st.success(f"✅ Low Risk of Churn ({result['churn_probability']:.2%})")

    except Exception as e:
        st.error("❌ Could not connect to API. Is FastAPI running?")
