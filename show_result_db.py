import sqlite3
class ShowResult_DB:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def create_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fraud_results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INT,
            merchant TEXT,
            category TEXT,
            amt REAL,
            gender TEXT,
            lat REAL,
            long REAL,
            city_pop INTEGER,
            job TEXT,
            unix_time INTEGER,
            merch_lat REAL,
            merch_long REAL,
            is_fraud BOOLEAN NULL
        )
        ''')
        conn.commit()
        conn.close()

    def insert_result_in_db(self, transaction, is_fraud):
        """
        Inserează un rezultat al tranzacției în baza de date fraud_results.
        
        Parameters:
        - transaction: Tuple care conține detaliile tranzacției.
        - is_fraud: Boolean care indică dacă tranzacția este frauduloasă.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO fraud_results (
           transaction_id, merchant, category, amt, gender, lat, long, city_pop, job, 
            unix_time, merch_lat, merch_long, is_fraud
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction[0],transaction[1], transaction[2], transaction[3], transaction[4],
            transaction[5], transaction[6], transaction[7], transaction[8],
            transaction[9],transaction[10], is_fraud
        ))
        conn.commit()
        conn.close()

