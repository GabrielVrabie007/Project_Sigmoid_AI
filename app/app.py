import streamlit as st
import numpy as np
import pandas as pd
# Side bar
with st.sidebar:
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        st.image("logo.png", width=100)
    with col2:
        st.markdown(
            "<h1 style='font-size:40px; margin:0; margin-bottom:10px;'>Finance</h1>",
            unsafe_allow_html=True
        )
    st.text(" ")
    if st.button("Fraud detection"):
        st.session_state.current_page = "Fraud detection"
