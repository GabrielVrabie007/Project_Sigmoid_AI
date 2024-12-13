import streamlit as st
import pandas as pd

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
        uf = pd.read_csv(uploaded_file)
        st.dataframe(uf)

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
