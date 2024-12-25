from fastapi import FastAPI, UploadFile, File
import pandas as pd
import joblib
from io import StringIO
from sklearn.preprocessing import LabelEncoder, StandardScaler
from fastapi.responses import StreamingResponse
import json
import asyncio
import random  

model = joblib.load("trained_models/fraud_detection_model.pkl")
label_encoder = joblib.load("trained_models/label_encoders.pkl")
scaler = joblib.load("trained_models/scaler.pkl")

app = FastAPI()

def preprocess_transaction(uf):
    if 'state' not in uf.columns:
        uf['state'] = 'default_value'

    label_columns = ['merchant', 'category', 'gender', 'job']
    for col in label_columns:
        if col in uf.select_dtypes(include=['object']).columns:
            if isinstance(label_encoder, dict) and col in label_encoder:
                encoder = label_encoder[col]
                uf[col] = encoder.transform(uf[col])
            else:
                return {"error": f"Label encoder pentru coloana '{col}' nu este disponibil în dicționarul furnizat."}

    categorical_columns = uf.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        uf[col] = uf[col].astype('category')

    uf.drop(columns=['Unnamed: 0', 'cc_num', 'city', 'zip', 'first', 'last', 'street', 'dob', 'trans_num', 'trans_date_trans_time', 'is_fraud'], inplace=True, errors='ignore')

    if 'state' in uf.columns:
        uf.drop(columns=['state'], inplace=True)

    numeric_columns = uf.select_dtypes(include=['int64', 'float64']).columns
    uf[numeric_columns] = scaler.transform(uf[numeric_columns])

    return uf

@app.post("/process-csv/")
async def process_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        data = StringIO(contents.decode("utf-8"))

        if not contents:
            return {"error": "Fișierul este gol!"}

        try:
            df = pd.read_csv(data)
        except Exception as e:
            return {"error": f"Eroare la citirea fișierului CSV: {str(e)}"}

        required_columns = ['merchant', 'category', 'gender', 'job']
        available_columns = [col for col in required_columns if col in df.columns]

        if not available_columns:
            return {"error": "Fișierul nu conține nicio coloană necesară pentru preprocesare."}

        df = df[available_columns]

        for col in required_columns:
            if col not in df.columns:
                df[col] = "default_value"

        processed_data = preprocess_transaction(df)

        if not isinstance(processed_data, pd.DataFrame):
            return processed_data

        async def generate_predictions():
            for index, row in processed_data.iterrows():
                row_data = row.values.reshape(1, -1)
                prediction = model.predict(row_data)[0]
                result = {"index": index, "fraud_prediction": int(prediction)}
                yield json.dumps(result) + "\n"
                await asyncio.sleep(random.randint(1, 10))

        return StreamingResponse(generate_predictions(), media_type="application/json")

    except Exception as e:
        return {"error": f"A apărut o eroare la procesarea fișierului: {str(e)}"}