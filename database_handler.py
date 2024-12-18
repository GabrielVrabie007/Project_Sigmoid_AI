import sqlite3

class DatabaseHandler:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_next_transaction(self): 
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, merchant, category, amt, gender, lat, long, city_pop, job, unix_time, merch_lat, merch_long
            FROM transactions 
            WHERE is_fraud IS NULL 
            LIMIT 1
        ''')
        row = cursor.fetchone()  # Preia un singur rând
        conn.close()
        
        return row  # Returnează rândul ca tuplu dacă există, altfel None