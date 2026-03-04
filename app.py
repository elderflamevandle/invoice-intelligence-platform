import streamlit as st
import pandas as pd
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from config import API_URL

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="Vendor Intelligence AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FastAPI Backend URL ---
# Managed centrally by config.py now

# -------------------------------------------------------
# Custom CSS for better aesthetics
# -------------------------------------------------------
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    h1 {color: #2c3e50;}
    .stAlert {border-radius: 10px;}
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #e67e22 !important;
    }
    .big-font {font-size:20px !important; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------------
# Header Section
# -------------------------------------------------------
st.title("🤖 Vendor Invoice Intelligence System")
st.markdown("""
Welcome to the AI-driven portal! Use the sidebar to switch between forecasting expected freight costs 
and evaluating the risk of incoming vendor invoices.
""")
st.divider()

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830305.png", width=100)
    st.title("Navigation")
    
    selected_model = st.radio(
        "Choose an AI Agent:",
        [
            "🚚 Freight Cost Predictor",
            "🚨 Anomaly Detector (Flagging)"
        ]
    )
    
    st.markdown("---")
    st.markdown("### System Status")
    try:
        # Quick health check to see if FastAPI is running
        res = requests.get(f"{API_URL}/docs", timeout=1)
        if res.status_code == 200:
            st.success("🟢 API Backend: Online")
        else:
            st.warning("🟡 API Backend: Unreachable")
    except:
        st.error("🔴 API Backend: Offline")
        st.caption("Ensure you run `python fastapi_app.py` in a separate terminal.")


# -------------------------------------------------------
# 1. Freight Cost Prediction
# -------------------------------------------------------
if selected_model == "🚚 Freight Cost Predictor":
    st.header("Forecasting Expected Freight Costs")
    
    with st.expander("ℹ️ How it works", expanded=False):
        st.info("Input the total dollar amount of an invoice. The Machine Learning model (Random Forest Regressor) will predict the expected shipping freight based on historical purchasing behaviors.")

    st.markdown("### Enter Invoice Information")
    
    with st.form("freight_form", border=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            dollars = st.number_input(
                "💰 Total Invoice Dollars ($)",
                min_value=1.0,
                value=18500.0,
                step=100.0,
                help="The total monetary value on the invoice."
            )
        
        submit_freight = st.form_submit_button("🔮 Predict Freight Cost", use_container_width=True)

    if submit_freight:
        with st.spinner("Calling AI Backend..."):
            try:
                # 1. Prepare JSON Payload
                payload = {"Dollars": dollars}
                
                # 2. Send Request to FastAPI
                response = requests.post(f"{API_URL}/predict_freight", json=payload)
                
                # 3. Handle Response
                if response.status_code == 200:
                    result = response.json()
                    prediction = result["Predicted_Freight"]
                    
                    st.success("Analysis Complete!")
                    st.metric(
                        label="Estimated Freight Cost", 
                        value=f"${prediction:,.2f}",
                        delta="Predicted"
                    )
                else:
                    st.error(f"Error from API: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Failed to connect to the FastAPI backend! Please make sure `uvicorn fastapi_app:app` is running.")


# -------------------------------------------------------
# 2. Invoice Flag Prediction
# -------------------------------------------------------
else:
    st.header("Invoice Risk Anomaly Detection")
    
    with st.expander("ℹ️ How it works", expanded=False):
        st.info("Input the invoice details. The AI Agent will evaluate historical operational patterns and flag the invoice if it detects anomalous costs, quantities, or freight charges requiring human audit.")

    st.markdown("### Enter Invoice Information")

    with st.form("invoice_flag_form", border=True):
        col1, col2 = st.columns(2)

        with col1:
            invoice_quantity = st.number_input("📦 Invoice Quantity", min_value=1, value=50)
            freight = st.number_input("🚚 Freight Cost ($)", min_value=0.0, value=1.73)
            total_item_quantity = st.number_input("📋 Total Item Quantity (PO)", min_value=1, value=162)

        with col2:
            invoice_dollars = st.number_input("💰 Invoice Dollars ($)", min_value=1.0, value=352.95)
            total_item_dollars = st.number_input("💵 Total Item Dollars (PO)", min_value=1.0, value=2476.0)

        st.markdown("<br>", unsafe_allow_html=True)
        submit_flag = st.form_submit_button("🛡️ Run AI Audit", use_container_width=True)

    if submit_flag:
        with st.spinner("Analyzing Vendor Patterns..."):
            try:
                # 1. Prepare JSON Payload
                payload = {
                    "invoice_quantity": invoice_quantity,
                    "invoice_dollars": invoice_dollars,
                    "Freight": freight,
                    "total_item_quantity": total_item_quantity,
                    "total_item_dollars": total_item_dollars
                }
                
                # 2. Send Request to FastAPI
                response = requests.post(f"{API_URL}/predict_invoice_flag", json=payload)
                
                # 3. Handle Response
                if response.status_code == 200:
                    result = response.json()
                    is_flagged = result["Requires_Manual_Approval"]
                    
                    if is_flagged:
                        st.error("🚨 **ALERT: High-Risk Invoice Detected**")
                        st.markdown("The AI recommends this invoice bypass auto-approval and requires **Manual Finance Audit**.")
                    else:
                        st.success("✅ **CLEARED: Invoice is Safe**")
                        st.markdown("The AI found no anomalies in this transaction. It is safe for auto-approval routing.")
                else:
                    st.error(f"Error from API: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Failed to connect to the FastAPI backend! Please make sure `fastapi_app.py` is running.")

