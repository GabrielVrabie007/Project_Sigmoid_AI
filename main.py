# from fastapi import FastAPI, HTTPException
# from fraud_detector import FraudDetector
# from first_version_with_database.data_loader import DataLoader
# from encoder_for_text_cols import process_transaction_data




# feature_names = [
#     "merchant", "category", "amt", "gender", "lat", "long", 
#     "city_pop", "job", "unix_time", "merch_lat", "merch_long"
# ]

# text_cols_in_db = ["merchant", "category", "gender", "job"]

# app = FastAPI()

# @app.get("/process-transaction/")
# def process_transaction():
#     try:
#         #unproccesed data o sa fie toate coloanele din csv file in format json
#         unprocecessed_transaction = get_next_transaction()
#         #transaction sa fie datele necesare pentru detectarea fraudei din feature names
#         transaction=unprocecessed_transaction[1:]
        
#         if not transaction:
#             raise HTTPException(status_code=404, detail="No more transactions to process")
        
#         print(f"Processing transaction: {transaction}")
#         #encoded_transaction_data sa fie datele din transaction encodate folosind LabelEncoder folosind fisierul cu path:
#         #('trained_models/label_encoders.pkl')
#         encoded_transaction_data = process_transaction_data(transaction,feature_names,text_cols)

#         is_fraud = fraud_detector.is_fraudulent(encoded_transaction_data)
#         #aici sa fie create in streamlit 2 tabele:tranzactii nefrauduloase si tranzactii frauduloase
#         result_db.insert_result_in_db(transaction,is_fraud)

#         return {"transaction_id": transaction_id, "is_fraud": is_fraud}
    
#     except HTTPException as e:
#         raise e
#     except Exception as e:

#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     process_transaction()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import json
import random
from joblib import load
import numpy as np
from fraud_detector import FraudDetector
import joblib
from encoder_for_text_cols import process_transaction_data
from extract_and_send_to_endpoint import process_file_and_send_data
from app.app import global_uf
from app.handler_result_tables import insert_data_in_tables
import streamlit as st


app = FastAPI()

fraud_detector = FraudDetector(
    model_path="trained_models/fraud_detection_model.pkl",
    scaler_path="trained_models/scaler.pkl"
)

feature_names = [
    "merchant", "category", "amt", "gender", "lat", "long", 
    "city_pop", "job", "unix_time", "merch_lat", "merch_long"
]

text_cols = ["merchant", "category", "gender", "job"]

def predict_columns(row, feature_names):
    """
    Selectează doar coloanele specificate în `feature_names` dintr-un rând.
    """
    selected_data = {feature: row[feature] for feature in feature_names if feature in row}
    return selected_data


@app.get("/process-transaction/")
def process_transaction():
    endpoint="http://localhost:8501/process-transaction/"
    try:
        unprocessed_transaction=process_file_and_send_data(global_uf,endpoint)

        transaction=predict_columns(unprocessed_transaction,feature_names)

        if not transaction:
            raise HTTPException(status_code=404, detail="No more transactions to process")

        print(f"Processing transaction: {transaction}")

        encoded_transaction_data = process_transaction_data(transaction,feature_names,text_cols)

        is_fraud = fraud_detector.is_fraudulent(encoded_transaction_data)

        insert_data_in_tables(unprocessed_transaction[0],predict_columns[2],is_fraud,unprocessed_transaction)

    except HTTPException as e:
         raise e
    except Exception as e:

         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


