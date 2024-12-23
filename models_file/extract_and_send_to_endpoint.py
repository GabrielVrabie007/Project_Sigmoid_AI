import requests
import random
import csv

def get_random_row(data):
    """
    Returnează un rând aleatoriu dintr-un fișier CSV.
    """
    with open(data, mode='r') as f:
        reader = list(csv.DictReader(f))
        random_index = random.randint(0, len(reader) - 1)
        return reader[random_index]

def send_data_to_endpoint(data, endpoint):
    """
    Trimite datele către endpoint folosind un POST request.
    """
    response = requests.post(endpoint, json=data)
    if response.status_code == 200:
        print(f"Data successfully sent to {endpoint}")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")

def process_file_and_send_data(row, endpoint):
    """
    Prezice daca tranzactia curenta este frauduoasa
    """
    while True:

        data = {
            "id": row["Unnamed: 0"],
            "trans_date_trans_time": row["trans_date_trans_time"],
            "cc_num": row["cc_num"],
            "merchant": row["merchant"],
            "category": row["category"],
            "amt": row["amt"],
            "first": row["first"],
            "last": row["last"],
            "gender": row["gender"],
            "street": row["street"],
            "city": row["city"],
            "state": row["state"],
            "zip": row["zip"],
            "lat": row["lat"],
            "long": row["long"],
            "city_pop": row["city_pop"],
            "job": row["job"],
            "dob": row["dob"],
            "trans_num": row["trans_num"],
            "unix_time": row["unix_time"],
            "merch_lat": row["merch_lat"],
            "merch_long": row["merch_long"],
            "is_fraud":None
        }
        
        send_data_to_endpoint(data, endpoint)
        return data