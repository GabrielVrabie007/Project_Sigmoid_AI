from fastapi import FastAPI, HTTPException
import joblib
from database_handler import DatabaseHandler
from fraud_detector import FraudDetector
from data_loader import DataLoader
from encoder_for_text_cols import process_transaction_data
from show_result_db import ShowResult_DB


feature_names = [
    "merchant", "category", "amt", "gender", "lat", "long", 
    "city_pop", "job", "unix_time", "merch_lat", "merch_long"
]

text_cols_in_db = ["merchant", "category", "gender", "job"]

app = FastAPI()

data_loader = DataLoader("transactions.db")
db_handler = DatabaseHandler("transactions.db")
fraud_detector = FraudDetector("trained_models/fraud_detection_model.pkl", "trained_models/scaler.pkl")

data_loader.load_csv_to_db("analysis/fraudTest.csv")

result_db=ShowResult_DB("fraud_results.db")
result_db.create_db()

@app.get("/process-transaction/")
def process_transaction():
    try:

        unprocecessed_transaction = db_handler.get_next_transaction()
        transaction_id = unprocecessed_transaction[0]
        transaction=unprocecessed_transaction[1:]
        print("-----------",transaction)
        if not transaction:
            raise HTTPException(status_code=404, detail="No more transactions to process")
        
        print(f"Processing transaction: {transaction}")

        encoded_transaction_data = process_transaction_data(transaction,feature_names,text_cols_in_db)

        joblib.dump(encoded_transaction_data, 'trained_models/encoded_transaction_data.pkl')
        print(encoded_transaction_data)

        is_fraud = fraud_detector.is_fraudulent(encoded_transaction_data)

        result_db.insert_result_in_db(transaction,is_fraud)

        return {"transaction_id": transaction_id, "is_fraud": is_fraud}
    
    except HTTPException as e:
        raise e
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    process_transaction()



