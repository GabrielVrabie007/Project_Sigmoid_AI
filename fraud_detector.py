import joblib
import numpy as np

class FraudDetector:
    def __init__(self, model_path: str, scaler_path: str):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def is_fraudulent(self, transaction_data):

        try:
            transaction_data = np.array(transaction_data)
            if transaction_data.ndim == 1:
                transaction_data = transaction_data.reshape(1, -1)

            scaled_data = self.scaler.transform(transaction_data)

            prediction = self.model.predict(scaled_data)

            return prediction[0] == 1
        
        except Exception as e:
            print(f"Error in fraud detection: {e}")
            return False


    

