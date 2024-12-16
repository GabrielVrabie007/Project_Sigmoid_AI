import sqlite3
import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def load_csv_to_db(self, csv_file: str):
        df = pd.read_csv(csv_file)
        
        if "is_fraud" in df.columns:
            df["is_fraud"] = np.nan
        
        
        column_mapping = {
            'Unnamed: 0': 'id',
            'trans_date_trans_time': 'trans_date_trans_time',
            'cc_num': 'cc_num',
            'merchant': 'merchant',
            'category': 'category',
            'amt': 'amt',
            'first': 'first',
            'last': 'last',
            'gender': 'gender',
            'street': 'street',
            'city': 'city',
            'state': 'state',
            'zip': 'zip',
            'lat': 'lat',
            'long': 'long',
            'city_pop': 'city_pop',
            'job': 'job',
            'dob': 'dob',
            'trans_num': 'trans_num',
            'unix_time': 'unix_time',
            'merch_lat': 'merch_lat',
            'merch_long': 'merch_long',
            'is_fraud': 'is_fraud',
            
        }
        
        df.rename(columns=column_mapping, inplace=True)
        
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trans_date_trans_time TEXT,
            cc_num TEXT,
            merchant TEXT,
            category TEXT,
            amt REAL,
            first TEXT,
            last TEXT,
            gender TEXT,
            street TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            lat REAL,
            long REAL,
            city_pop INTEGER,
            job TEXT,
            dob TEXT,
            trans_num TEXT,
            unix_time INTEGER,
            merch_lat REAL,
            merch_long REAL,
            is_fraud BOOLEAN NULL
        )
        ''')
        
        df.to_sql("transactions", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
