from sklearn.preprocessing import LabelEncoder
import pandas as pd

def process_transaction_data(transaction_tuple, feature_names, categorical_columns):
    if len(transaction_tuple) != len(feature_names):
        raise ValueError("Dimensiunea tuplului nu corespunde cu numele caracteristicilor.")
    df = pd.DataFrame([transaction_tuple], columns=feature_names)
    
    for column in categorical_columns:
        if column in df.columns:
            encoder = LabelEncoder()
            df[column] = encoder.transform(df[column])
        else:
            raise ValueError(f"Coloana '{column}' nu există în DataFrame.")
    
    return df





