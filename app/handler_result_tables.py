import streamlit as st
import pandas as pd

def create_tables():
    table1 = pd.DataFrame()
    table2 = pd.DataFrame()

    table_style = {
        'background-color': 'rgba(0, 123, 255, 0.1)',
        'color': 'black', 
        'border-color': '#dee2e6', 
        'border-radius': '10px', 
        'padding': '10px', 
        'font-family': 'Arial, sans-serif'  
    }

    styled_table1 = table1.style.set_properties(**{
        'background-color': 'rgba(0, 123, 255, 0.1)', 
        'color': 'black', 
        'border-color': '#dee2e6',  
        'border-radius': '10px',
        'font-family': 'Arial, sans-serif',  
        'padding': '10px'
    }).set_table_styles([
        {'selector': 'thead', 'props': [('background-color', 'rgba(0, 123, 255, 0.3)'), ('color', 'white')]}, 
        {'selector': 'tbody', 'props': [('background-color', 'rgba(0, 123, 255, 0.1)')]},  
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]}  
    ])
    
    styled_table2 = table2.style.set_properties(**{
        'background-color': 'rgba(0, 123, 255, 0.1)',
        'color': 'black',
        'border-color': '#dee2e6', 
        'border-radius': '10px',
        'font-family': 'Arial, sans-serif',
        'padding': '10px'
    }).set_table_styles([
        {'selector': 'thead', 'props': [('background-color', 'rgba(0, 123, 255, 0.3)'), ('color', 'white')]},  
        {'selector': 'tbody', 'props': [('background-color', 'rgba(0, 123, 255, 0.1)')]},  
        {'selector': 'th', 'props': [('text-align', 'center')]},  
        {'selector': 'td', 'props': [('text-align', 'center')]} 
    ])
    
    st.write("### Legal Transactions: Results")
    st.dataframe(styled_table1)

    st.write("### Fraudulous Transactions: Results")
    st.dataframe(styled_table2)

def insert_data_in_tables(ID, amount, is_fraud, data):
    data_filtered = pd.DataFrame({
        'ID': [ID],
        'Amount': [amount],
        'is_fraud': [is_fraud]
    })

    if bool(is_fraud == 1):
        st.write("### Fraudulous Transactions: Results")
        st.dataframe(data_filtered)
    else:
        st.write("### Legal Transactions: Results")
        st.dataframe(data_filtered)

