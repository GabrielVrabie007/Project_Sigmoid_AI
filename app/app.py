import streamlit as st
import pandas as pd
import joblib
from handler_result_tables import create_tables
import sys
from pathlib import Path
sys.path.append(r"D:/Machine_Learning/Project_Sigmoid_AI")
from extract_and_send_to_endpoint import *
from encoder_for_text_cols import process_transaction_data
from fraud_detector import FraudDetector
from handler_result_tables import insert_data_in_tables
import time

@st.cache_resource
def load_model():
    return joblib.load("trained_models/fraud_detection_model.pkl")

model = load_model()

feature_names = [
    "merchant", "category", "amt", "gender", "lat", "long", 
    "city_pop", "job", "unix_time", "merch_lat", "merch_long"
]

text_cols = ["merchant", "category", "gender", "job"]

fraud_detector = FraudDetector(
    model_path="trained_models/fraud_detection_model.pkl",
    scaler_path="trained_models/scaler.pkl"
)

global global_uf

def validate_columns():
    
    required_columns = ['merchant', 'category', 'amt', 'gender', 'lat', 'long', 
                        'city_pop', 'job', 'unix_time', 'merch_lat', 'merch_long']
    
    missing_columns = [col for col in required_columns if col not in global_uf.columns]
    if missing_columns:
        st.error(f"Fișierul nu conține următoarele coloane necesare pentru predicție: {', '.join(missing_columns)}")
        st.stop()
        return False
    st.success("Toate coloanele necesare pentru predicție sunt prezente.")
    return True

def home():
    st.markdown(
        "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Welcome to Finance</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h1 style='font-size:20px; margin:0; width:100%; text-align:center;'>Open the sidebar and choose a feature</h1>",
        unsafe_allow_html=True
    )


def upload_csv():
    uploaded_file = st.file_uploader("Upload a CSV", type='csv')
    if uploaded_file:
        try:
            global_uf = pd.read_csv(uploaded_file, sep=None, engine='python')
            global_uf.columns = global_uf.columns.str.strip()
            
            if st.session_state["page"] == "Fraud Detection":
                st.write("Coloanele din fișierul încărcat sunt:", list(global_uf.columns))
                st.dataframe(global_uf.head())
        except Exception as e:
            st.error(f"Fișierul nu poate fi citit: {str(e)}")
            st.stop()
            return True
        
def fraud_detection():
    st.markdown(
        "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Fraud Detection</h1>",
        unsafe_allow_html=True
    )
    loaded_csv=upload_csv()
    if loaded_csv==True:
        required_columns=validate_columns()

        X_input = global_uf[required_columns]

        try:
            predictions = model.predict(X_input)
        except Exception as e:
            st.error(f"A apărut o eroare la efectuarea predicțiilor: {str(e)}")
            st.stop()

        global_uf['Fraud Prediction'] = predictions
        st.write("Rezultatele predicțiilor:")
        st.dataframe(global_uf)

        st.markdown("### Statistici despre predicții")
        fraud_count = global_uf['Fraud Prediction'].value_counts()
        st.bar_chart(fraud_count)

def real_data_time_generator():
    st.markdown(
        "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Real Data Time Generator</h1>",
        unsafe_allow_html=True
    )
    st.write("This page is simulating real time encoming data for detecting fraud transactions")
    # Exemplu de implementare a funcționalității personalizate
    data=upload_csv()
    if st.button("Generate Data") and data:
        st.write("Waiting for results...")

        while True:
            unfiltred_data=process_file_and_send_data(data,endpoint="http://localhost:8501")
            ID = unfiltred_data.get('', None)
            required_columns=validate_columns()

            encoded_transaction_data = process_transaction_data(data,feature_names,text_cols)

            is_fraud = fraud_detector.is_fraudulent(encoded_transaction_data)

            insert_data_in_tables(ID,required_columns[2],is_fraud,required_columns)
            time.sleep(15)
    else:
        st.write("Click me!")

if "page" not in st.session_state:
    st.session_state["page"] = "Home"

with st.sidebar:
    with st.container():
        col1, col2 = st.columns([1, 2], gap="small")
        with col1:
            st.image("app/logo.png", width=100)
        with col2:
            st.markdown(
                "<h1 style='font-size:40px; margin:0; margin-top:10px;'>Finance</h1>",
                unsafe_allow_html=True
            )

    st.markdown("<hr style='margin:20px 0; border:1px solid lightgray;'/>", unsafe_allow_html=True)

    st.write("# Features")
    if st.button("Home"):
        st.session_state["page"] = "Home"
    if st.button("Fraud Detection"):
        st.session_state["page"] = "Fraud Detection"
    if st.button("Real Data Time Generator"):
        st.session_state["page"] = "Real Data Time Generator"

# Page Routing
if st.session_state["page"] == "Home":
    home()
elif st.session_state["page"] == "Fraud Detection":
    fraud_detection()
elif st.session_state["page"] == "Real Data Time Generator":
    real_data_time_generator()
    create_tables()
    
    
    
