import json
import random
from datetime import datetime, timedelta
import time
from kafka import KafkaProducer

# Lista województw w Polsce
wojewodztwa = [
    "dolnośląskie", "kujawsko-pomorskie", "lubelskie", "lubuskie", "łódzkie", 
    "małopolskie", "mazowieckie", "opolskie", "podkarpackie", "podlaskie", 
    "pomorskie", "śląskie", "świętokrzyskie", "warmińsko-mazurskie", 
    "wielkopolskie", "zachodniopomorskie"
]

def generate_person_data():
    t = datetime.now() + timedelta(seconds=random.randint(-15, 0))
    
    person_data = {
        "time": str(t),
        "country": "Poland",
        "province": random.choice(wojewodztwa),  # Województwo
        "age": random.randint(1, 100),
        "gender": random.choice(["male", "female"]),
        "covid_positive": random.choice([0, 1]),  # 0 - brak COVID-19, 1 - stwierdzony COVID-19
        "fever": random.choice([True, False]),
        "cough": random.choice([True, False]),
        "shortness_of_breath": random.choice([True, False]),
        "muscle_pain": random.choice([True, False]),
        "loss_of_taste_or_smell": random.choice([True, False]),
        "sore_throat": random.choice([True, False]),
        "fatigue": random.choice([True, False]),
        "headache": random.choice([True, False]),
        "chills": random.choice([True, False]),
        "diarrhea": random.choice([True, False]),
        "vaccinated": random.choice([True, False]),
        "temperature": round(random.uniform(35.5, 40.0), 1),  # Temperatura ciała
        "blood_pressure": random.randint(90, 150),  # Ciśnienie krwi (górne)
        "heart_rate": random.randint(60, 100),  # Tętno
        "oxygen_saturation": random.randint(90, 100)  # Nasycenie tlenu
    }
    
    return person_data

if __name__ == "__main__":
    SERVER = "localhost:9092"  # Adres i port brokera Kafka
    
    producer = KafkaProducer(bootstrap_servers=[SERVER],
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    
    while True:
        person_data = generate_person_data()
        producer.send('covid_data_topic', value=person_data)
        print("Sent data:", person_data)
        time.sleep(1.5)
