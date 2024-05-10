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

@app.route('/chart')
def chart():
    return jsonify(data_from_kafka)

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


