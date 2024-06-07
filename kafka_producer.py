import json
import random
from datetime import datetime, timedelta
import time
from kafka import KafkaProducer

wojewodztwa = [
    "dolnośląskie", "kujawsko-pomorskie", "lubelskie", "lubuskie", "łódzkie", 
    "małopolskie", "mazowieckie", "opolskie", "podkarpackie", "podlaskie", 
    "pomorskie", "śląskie", "świętokrzyskie", "warmińsko-mazurskie", 
    "wielkopolskie", "zachodniopomorskie"
]

record_count = 0
start_date = datetime.now()

def generate_person_data():
    days_ago = 14 - (record_count // 200)
    base_time = start_date - timedelta(days=days_ago)
    t = base_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=random.randint(0, 86399))
    
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
        "temperature": round(random.uniform(35.5, 40.0), 1),
        "blood_pressure": random.randint(90, 150),
        "heart_rate": random.randint(60, 100),
        "oxygen_saturation": random.randint(90, 100)
    }
    # ZMIENNA DEATH MOZE PRZYJAC 1 TYLKO WTEDY KIEDY OSOBA ZACHOROWALA NA COVIDA (covid_positive = 1)
    person_data["death"] = 1 if random.choice([0, 1]) == 1 and person_data["covid_positive"] == 1 else 0
    # ZMIENNA RECOVERED MOZE PRZYJAC 1 TYLKO WTEDY KIEDY OSOBA ZACHOROWALA NA COVIDA (covid_positive = 1) I NIE ZMARLA (death = 0)
    person_data["recovered"] = random.choice([0, 1]) if person_data["covid_positive"] == 1 and person_data["death"] == 0 else 0
    
    return person_data

if __name__ == "__main__":
    SERVER = "localhost:9092"
    
    producer = KafkaProducer(bootstrap_servers=[SERVER],
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    
    while True:
        person_data = generate_person_data()
        if random.random() < 0.8:
            producer.send('covid_data_topic', value=person_data)
            print("Sent data:", person_data)
        else:
            print("Data not sent")
            
        record_count += 1
        time.sleep(0.5)
