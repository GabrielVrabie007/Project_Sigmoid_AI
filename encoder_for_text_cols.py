from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib

def process_transaction_data(transaction_tuple, feature_names, categorical_columns):
    encoders = joblib.load('trained_models/label_encoders.pkl')
    if len(transaction_tuple) != len(feature_names):
        raise ValueError("Dimensiunea tuplului nu corespunde cu numele caracteristicilor.")
    
    df = pd.DataFrame([transaction_tuple], columns=feature_names)
    print("Columns in input DataFrame:", df.columns)
    for column in categorical_columns:
        if column in df.columns:
            if column in encoders:
                df[column] = encoders[column].transform(df[column])
            else:
                raise ValueError(f"Encoderul pentru coloana '{column}' nu a fost găsit.")
        else:
            raise ValueError(f"Coloana '{column}' nu există în DataFrame.")
    
    return df





