from flask import Flask, render_template, jsonify
from kafka import KafkaConsumer
import json
from threading import Thread
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

data_from_kafka = []

def kafka_consumer():
    SERVER = "localhost:9092"
    TOPIC = "covid_data_topic"

    consumer = KafkaConsumer(TOPIC,
                             bootstrap_servers=[SERVER],
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    for message in consumer:
        data = message.value
        data_from_kafka.append(data)
        df = pd.DataFrame(data_from_kafka)
        print(df)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data_summary')
def data():
    df = pd.DataFrame(data_from_kafka)
    df_cases = len(df['covid_positive'])
    df_infected = len(df.loc[df['covid_positive'] == 1])
    df_recovered = len(df.loc[df['recovered'] == 1])
    df_death = len(df.loc[df['death'] == 1])
    df_active = df_infected - df_recovered - df_death

    return jsonify({"active": df_active, "deaths": df_death, "recovered": df_recovered, "cases": df_cases})

@app.route('/number_cases')
def chart():
    df = pd.DataFrame(data_from_kafka)
    df_infected = df.loc[df['covid_positive'] == 1]
    num_infected = len(df_infected)

    num_recovered = len(df_infected.loc[df_infected['recovered'] == 1])
    num_death = len(df_infected.loc[df_infected['death'] == 1])
    num_active = num_infected - num_recovered - num_death

    labels = ['Active', 'Death', 'Recovered']
    sizes = [num_active, num_death, num_recovered]

    return jsonify({"labels": labels, "sizes": sizes})

@app.route('/age_histogram')
def table():
    df = pd.DataFrame(data_from_kafka)
    bins = [1, 18, 30, 50, 70, 80, 100]
    df['age_group'] = pd.cut(df['age'], bins)
    df_age_grouped = df.loc[df['covid_positive'] == 1].groupby('age_group').size().reset_index(name='count')
    df_age_grouped['age_group_str'] = df_age_grouped['age_group'].apply(lambda x: f"{x.left}-{x.right}")

    age_groups = df_age_grouped['age_group_str'].tolist()
    count_sum = df_age_grouped['count'].tolist()

    return jsonify({"age_groups": age_groups, "count_sum": count_sum})

@app.route('/chart_provinces')
def model():
    df = pd.DataFrame(data_from_kafka)
    df = df.loc[df['covid_positive'] == 1]
    df_grouped = df.groupby('province').size().reset_index(name='count')

    provinces = df_grouped['province'].tolist()
    count_sum = df_grouped['count'].tolist()

    return jsonify({"provinces": provinces, "count_sum": count_sum})

if __name__ == "__main__":
    kafka_thread = Thread(target=kafka_consumer)
    kafka_thread.daemon = True
    kafka_thread.start()  # Uruchamianie konsumenta w osobnym wątku
    app.run(debug=True, port=5000)


