import streamlit as st
import numpy as np
import pandas as pd
import nbformat
from nbconvert import PythonExporter


# Side bar
with st.sidebar:
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        st.image("app/logo.png", width=100)
    with col2:
        st.markdown(
            "<h1 style='font-size:40px; margin:0; margin-bottom:10px;'>Finance</h1>",
            unsafe_allow_html=True
        )
    st.text(" ")
    st.session_state.current_page = st.radio("Features:", ["Home","Fraud detection"])

def home():
    st.markdown(
            "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Welcome to Finance</h1>",
            unsafe_allow_html=True
    )
    st.markdown(
            "<h1 style='font-size:20px; margin:0; width:100%; text-align:center;'>Open the sidebar and choose a feature</h1>",
            unsafe_allow_html=True
    )

# Fraud detection
def fraud_detection():
    st.markdown(
            "<h1 style='font-size:40px; margin:0; width:100%; text-align:center;'>Fraud Detection</h1>",
            unsafe_allow_html=True
    )
    col1, col2 = st.columns([2,1], vertical_alignment="center")
    with col1:
        st.write("Tab")
    with col2:
        uploaded_file = st.file_uploader("Upload a CSV", type='csv')
        if uploaded_file is not None:
            uf = pd.read_csv(uploaded_file)
            cl = uf



# Nav system
if st.session_state.current_page == "Home":
    home()
elif st.session_state.current_page == "Fraud detection":
    fraud_detection()

