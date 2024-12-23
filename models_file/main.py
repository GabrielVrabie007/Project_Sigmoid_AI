from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from joblib import load
import numpy as np
from fraud_detector import FraudDetector
from encoder_for_text_cols import process_transaction_data
from extract_and_send_to_endpoint import process_file_and_send_data
import uvicorn
from requests import request


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


@app.post("/process-transaction/")
def process_transaction(): 
    try:
        data = request.json()

        df = pd.DataFrame(data)

        row = df.iloc[0].values

        is_fraud = fraud_detector.is_fraudulent(row)

        return JSONResponse(status_code=200, content={"is_fraud": is_fraud})

    except HTTPException as e:
         raise e
    except Exception as e:

         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501, log_level="info")
