import streamlit as st
import pandas as pd
import joblib


@st.cache_resource
def load_model():
    return joblib.load("trained_models/fraud_detection_model.pkl")



model = load_model()
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
            # Încărcarea fișierului, cu delimitator flexibil (tab sau virgulă)
            uf = pd.read_csv(uploaded_file, sep=None, engine='python')  # Pandas detectează automat separatorul
            uf.columns = uf.columns.str.strip()  # Curăță spațiile suplimentare din numele coloanelor

            st.write("Coloanele din fișierul încărcat sunt:", list(uf.columns))
            st.dataframe(uf.head())  # Afișează primele rânduri din fișier
        except Exception as e:
            st.error(f"Fișierul nu poate fi citit: {str(e)}")
            st.stop()  # Oprește execuția dacă fișierul e invalid

        # Verifică dacă fișierul conține toate coloanele necesare
        required_columns = ['merchant', 'category', 'amt', 'gender', 'lat', 'long', 
                            'city_pop', 'job', 'unix_time', 'merch_lat', 'merch_long']
        missing_columns = [col for col in required_columns if col not in uf.columns]

        if missing_columns:
            st.error(f"Fișierul nu conține următoarele coloane necesare pentru predicție: {', '.join(missing_columns)}")
            st.stop()

        st.success("Toate coloanele necesare pentru predicție sunt prezente.")

        # Pregătește datele pentru predicție
        X_input = uf[required_columns]

        # Efectuează predicția
        try:
            predictions = model.predict(X_input)
        except Exception as e:
            st.error(f"A apărut o eroare la efectuarea predicțiilor: {str(e)}")
            st.stop()

        # Adaugă predicțiile în dataframe
        uf['Fraud Prediction'] = predictions
        st.write("Rezultatele predicțiilor:")
        st.dataframe(uf)

        # Afișează statistici despre predicții
        st.markdown("### Statistici despre predicții")
        fraud_count = uf['Fraud Prediction'].value_counts()
        st.bar_chart(fraud_count)



if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# Sidebar
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

if st.session_state["page"] == "Home":
    home()
elif st.session_state["page"] == "Fraud Detection":
    fraud_detection()
