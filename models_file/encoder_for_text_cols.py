from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib

def process_transaction_data(data,required_columns, text_cols):
    encoders = joblib.load('trained_models/label_encoders.pkl')
    if len(data) != len(required_columns):
        print(data)
        raise ValueError("Dimensiunea tuplului nu corespunde cu numele caracteristicilor.")
    
    df = pd.DataFrame([data], columns=required_columns)
    print("Columns in input DataFrame:", df.columns)
    for column in text_cols:
        if column in df.columns:
            if column in encoders:
                df[column] = encoders[column].transform(df[column])
            else:
                raise ValueError(f"Encoderul pentru coloana '{column}' nu a fost găsit.")
        else:
            raise ValueError(f"Coloana '{column}' nu există în DataFrame.")
    
    return df





