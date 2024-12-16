from fastapi import FastAPI, HTTPException
from database_handler import DatabaseHandler
from fraud_detector import FraudDetector
from data_loader import DataLoader
from encoder_for_text_cols import process_transaction_data


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

@app.get("/process-transaction/")
def process_transaction():
    try:

        transaction = db_handler.get_next_transaction()
        if not transaction:
            raise HTTPException(status_code=404, detail="No more transactions to process")
        
        print(f"Processing transaction: {transaction}")

        encoded_transaction_data = process_transaction_data(transaction,feature_names,text_cols_in_db)
        print(encoded_transaction_data)

        is_fraud = fraud_detector.is_fraudulent(encoded_transaction_data)

        db_handler.update_transaction(transaction[0], is_fraud)

        return {"transaction_id": transaction[0], "is_fraud": is_fraud}
    
    except HTTPException as e:
        raise e
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    process_transaction()



