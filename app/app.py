import streamlit as st
import pandas as pd
import joblib
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handler_result_tables import create_tables, insert_data_in_tables  
from models_file.extract_and_send_to_endpoint import *
from models_file.encoder_for_text_cols import process_transaction_data
from models_file.fraud_detector import FraudDetector
import time

# Încarcă modelul
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
            
            if st.session_state["page"] == "Card Fraud Detection":
                st.write("Coloanele din fișierul încărcat sunt:", list(global_uf.columns))
                st.dataframe(global_uf.head())
        except Exception as e:
            st.error(f"Fișierul nu poate fi citit: {str(e)}")
            st.stop()
            return True

def card_fraud_detection():
    st.markdown(
        "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Card Fraud Detection</h1>",
        unsafe_allow_html=True
    )
    # Se alege funcționalitatea dorită
    mode = st.radio("Selectează modul de detectare a fraudelor", 
                    ("Real-Time Fraud Detection", "Fraud Detection din CSV"))

    if mode == "Fraud Detection din CSV":
        st.write("Încarcă fișierul CSV cu tranzacții.")
        loaded_csv = upload_csv()
        if loaded_csv:
            required_columns = validate_columns()

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
    
    if mode == "Real-Time Fraud Detection":
        real_data_time_generator()

def real_data_time_generator():
    st.markdown(
        "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Real-Time Fraud Detection</h1>",
        unsafe_allow_html=True
    )
    st.write("Simulăm tranzacții care vin într-un interval de timp și le procesăm pentru a detecta fraudele.")
    data = upload_csv()
    
    if st.button("Generate Data") and data:
        st.write("Așteptăm rezultate...")

        while True:
            # Tranzacții simulate
            unfiltred_data = process_file_and_send_data(data, endpoint="http://localhost:8501")
            ID = unfiltred_data.get('', None)
            required_columns = validate_columns()

            encoded_transaction_data = process_transaction_data(data, feature_names, text_cols)

            is_fraud = fraud_detector.is_fraudulent(encoded_transaction_data)

            insert_data_in_tables(ID, required_columns[2], is_fraud, required_columns)
            time.sleep(15)  # Așteptăm 15 secunde între fiecare tranzacție
    else:
        st.write("Apasă pe butonul pentru a genera tranzacții!")

# Sidebar pentru navigare
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
    if st.button("Card Fraud Detection"):
        st.session_state["page"] = "Card Fraud Detection"

# Routing pentru pagini
if st.session_state["page"] == "Home":
    home()
elif st.session_state["page"] == "Card Fraud Detection":
    card_fraud_detection()
