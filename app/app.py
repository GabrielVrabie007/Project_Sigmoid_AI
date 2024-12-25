import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
import requests
import json

#!!!!!!!!!!!!!!!TODO Partea cu real-time fraud detection este in proces si posibil sa nu functioneze corect
#TODO 

@st.cache_resource
def load_model():
    model = joblib.load("trained_models/fraud_detection_model.pkl")
    label_encoder = joblib.load("trained_models/label_encoders.pkl")
    scaler = joblib.load("trained_models/scaler.pkl")
    return model, label_encoder, scaler

model, label_encoder, scaler = load_model()

def home():
    st.markdown(
        "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Welcome to Finance</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h1 style='font-size:20px; margin:0; width:100%; text-align:center;'>Open the sidebar and choose a feature</h1>",
        unsafe_allow_html=True
    )

def fraud_detection():
    st.markdown(
        "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Fraud Detection</h1>",
        unsafe_allow_html=True
    )
    uploaded_file = st.file_uploader("Upload a CSV", type='csv')
    if uploaded_file is not None:
        try:
            uf = pd.read_csv(uploaded_file, sep=None, engine='python')
            uf.columns = uf.columns.str.strip()

            st.write("Coloanele din fișierul încărcat sunt:", list(uf.columns))
            st.dataframe(uf.head()) 
        except Exception as e:
            st.error(f"Fișierul nu poate fi citit: {str(e)}")
            st.stop()

        required_columns = ['merchant', 'category', 'amt', 'gender', 'lat', 'long', 
                            'city_pop', 'job', 'unix_time', 'merch_lat', 'merch_long']
        missing_columns = [col for col in required_columns if col not in uf.columns]

        if missing_columns:
            st.error(f"Fișierul nu conține următoarele coloane necesare pentru predicție: {', '.join(missing_columns)}")
            st.stop()

        st.success("Toate coloanele necesare pentru predicție sunt prezente.")
        uf_original = uf.copy()

        label_columns = ['merchant', 'category', 'gender', 'job']
        for col in label_columns:
            if col in uf.select_dtypes(include=['object']).columns:
                if isinstance(label_encoder, dict) and col in label_encoder:
                    encoder = label_encoder[col]
                    uf[col] = encoder.transform(uf[col])
                else:
                    st.error(f"Label encoder pentru coloana '{col}' nu este disponibil în dicționarul furnizat.")
                    st.stop()
      
        uf.drop(columns=['Unnamed: 0','cc_num','city','zip','first', 'last', 'street','dob', 'trans_num','trans_date_trans_time', 'is_fraud'],inplace=True)
        numeric_columns = uf.select_dtypes(include=['int64', 'float64']).columns
        uf[numeric_columns] = scaler.transform(uf[numeric_columns])

        X_input = uf[required_columns]

        try:
            predictions = model.predict(X_input)
        except Exception as e:
            st.error(f"A apărut o eroare la efectuarea predicțiilor: {str(e)}")
            st.stop()

        uf['Fraud Prediction'] = predictions
        fraud_rows = uf[uf['Fraud Prediction'] == 1]
        st.markdown("### Rânduri frauduloase detectate:")
        columns_to_scale= ["merchant", "category", "amt", "gender", "lat", "long", "city_pop", "job", "unix_time", "merch_lat", "merch_long"]
        fraud_rows[columns_to_scale] = scaler.inverse_transform(fraud_rows[columns_to_scale])

        st.dataframe(fraud_rows)
        st.markdown("### Statistici despre predicții")
        fraud_count = uf['Fraud Prediction'].value_counts()
        st.bar_chart(fraud_count)

def real_time_fraud_detection():
    st.markdown(
        "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Real-Time Fraud Detection</h1>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Upload your CSV file", type='csv')
    if uploaded_file is not None:
        try:
            response = requests.post("http://127.0.0.1:8000/process-csv/", files={"file": uploaded_file}, stream=True)

            if response.status_code == 200:
                st.write("Predicțiile vor fi afișate în timp real...")
                predictions_container = st.empty()
                predictions = []
                st.write("Coloanele din fișierul încărcat sunt:", response.content)
                for line in response.iter_lines():
                    if line:
                        result = json.loads(line.decode("utf-8"))
                        predictions.append(result)
                        predictions_df = pd.DataFrame(predictions)

                        predictions_df['Fraud Smiley'] = predictions_df['fraud_prediction'].apply(
                            lambda x: "😡" if x == 1 else "🙂"
                        )

                        predictions_container.dataframe(predictions_df)

            else:
                st.error("A apărut o eroare: " + response.json().get("error", "Necunoscut"))

        except Exception as e:
            st.error(f"Fișierul nu poate fi trimis: {str(e)}")
    else:
        st.info("Te rugăm să încarci un fișier CSV pentru procesare.")

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
    page_selection = st.selectbox("Alege o funcționalitate", ["Home", "Fraud Detection", "Real-Time Fraud Detection"])

    if page_selection == "Home":
        st.session_state["page"] = "Home"
    elif page_selection == "Fraud Detection":
        st.session_state["page"] = "Fraud Detection"
    elif page_selection == "Real-Time Fraud Detection":
        st.session_state["page"] = "Real-Time Fraud Detection"

if st.session_state["page"] == "Home":
    home()
elif st.session_state["page"] == "Fraud Detection":
    fraud_detection()
elif st.session_state["page"] == "Real-Time Fraud Detection":
    real_time_fraud_detection()