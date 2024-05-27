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
        # print(df)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time_chart')
def time_chart():
    df = pd.DataFrame(data_from_kafka)
    df['time'] = pd.to_datetime(df['time'])

    df_infected = df.loc[df['covid_positive'] == 1]
    df_active = df_infected[(df_infected['recovered'] == 0) & (df_infected['death'] == 0)]
    active_cases = df_active.groupby(df['time'].dt.strftime('%Y-%m-%d')).size()
    recovered_cases = df_infected.loc[df_infected['recovered'] == 1].groupby(df['time'].dt.strftime('%Y-%m-%d')).size()
    death_cases = df_infected.loc[df_infected['death'] == 1].groupby(df['time'].dt.strftime('%Y-%m-%d')).size()

    time_a = active_cases.index.tolist()
    active_cases = active_cases.tolist()
    time_r = recovered_cases.index.tolist()
    recovered_cases = recovered_cases.tolist()
    time_d = death_cases.index.tolist()
    death_cases = death_cases.tolist()

    return jsonify({"time_a": time_a, "active_cases": active_cases, "time_r": time_r, "recovered_cases": recovered_cases, "time_d": time_d, "death_cases": death_cases})


@app.route('/data_summary')
def data():
    df = pd.DataFrame(data_from_kafka)
    df_cases = len(df['covid_positive'])
    df_infected = len(df.loc[df['covid_positive'] == 1])
    df_recovered = len(df.loc[df['recovered'] == 1])
    df_death = len(df.loc[df['death'] == 1])
    df_active = df_infected - df_recovered - df_death


    df_cp = df.loc[df['covid_positive'] == 1]
    death_rate = round((df_cp['death'] == 1).mean() * 100)
    recovery_rate = round((df_cp['recovered'] == 1).mean() * 100)
    mean_age_infected = round(df.loc[df['covid_positive'] == 1, 'age'].mean())
    mean_temperature_infected = round(df.loc[df['covid_positive'] == 1, 'temperature'].mean())
    mean_blood_pressure_infected = round(df.loc[df['covid_positive'] == 1, 'blood_pressure'].mean())
    mean_heart_rate_infected = round(df.loc[df['covid_positive'] == 1, 'heart_rate'].mean())
    mean_oxygen_saturation_infected = round(df.loc[df['covid_positive'] == 1, 'oxygen_saturation'].mean())

    temperatures_infected = df.loc[df['covid_positive'] == 1, 'temperature']
    std_temperature_infected = round(temperatures_infected.std())

    return jsonify({"active": df_active, "deaths": df_death, "recovered": df_recovered, "cases": df_cases, "death_rate": death_rate, "recovery_rate": recovery_rate, "mean_age_infected": mean_age_infected, "mean_temperature_infected": mean_temperature_infected, "mean_blood_pressure_infected": mean_blood_pressure_infected, "mean_heart_rate_infected": mean_heart_rate_infected, "mean_oxygen_saturation_infected": mean_oxygen_saturation_infected, "std_temperature_infected": std_temperature_infected})

@app.route('/number_cases')
def chart():
    df = pd.DataFrame(data_from_kafka)
    df_infected = df.loc[df['covid_positive'] == 1]
    num_infected = len(df_infected)

    num_recovered = len(df_infected.loc[df_infected['recovered'] == 1])
    num_death = len(df_infected.loc[df_infected['death'] == 1])
    num_active = num_infected - num_recovered - num_death

    labels = ['Active', 'Death', 'Recovered', ]
    sizes = [num_active, num_death, num_recovered]

    return jsonify({"labels": labels, "sizes": sizes})

@app.route('/age_histogram')
def table():
    df = pd.DataFrame(data_from_kafka)
    bins = [1, 18, 30, 50, 70, 80, 100]
    df['age_group'] = pd.cut(df['age'], bins)

    age_group_summary = df[df['covid_positive'] == 1].groupby('age_group').agg(
    Active=('death', lambda x: sum((x == 0) & (df['recovered'] == 0))),
    Death=('death', 'sum'),
    Recovered=('recovered', 'sum')
    ).reset_index()

    age_group_summary['age_group_str'] = age_group_summary['age_group'].apply(lambda x: f"{int(x.left)}-{int(x.right)}")

    age_groups = age_group_summary['age_group_str'].tolist()
    active = age_group_summary['Active'].tolist()
    deaths = age_group_summary['Death'].tolist()
    recovered = age_group_summary['Recovered'].tolist()

    return jsonify({"age_groups": age_groups, "active": active, "deaths": deaths, "recovered": recovered})

@app.route('/chart_provinces')
def model():
    df = pd.DataFrame(data_from_kafka)

    df_c = df.loc[df['covid_positive'] == 1]
    df_active = df_c[(df_c['recovered'] == 0) & (df_c['death'] == 0)]
    active_cases_by_province = df_active.groupby('province').size()
    recovered_by_province = df_c[df_c['recovered'] == 1].groupby('province').size()
    deaths_by_province = df_c[df_c['death'] == 1].groupby('province').size()

    result = pd.DataFrame({
    'active_cases': active_cases_by_province,
    'recovered': recovered_by_province,
    'deaths': deaths_by_province
    }).fillna(0).astype(int).reset_index()

    provinces = result['province'].tolist()
    active = result['active_cases'].tolist()
    recovered = result['recovered'].tolist()
    deaths = result['deaths'].tolist()

    return jsonify({"provinces": provinces, "active": active, "recovered": recovered, "deaths": deaths})

if __name__ == "__main__":
    kafka_thread = Thread(target=kafka_consumer)
    kafka_thread.daemon = True
    kafka_thread.start()  # Uruchamianie konsumenta w osobnym wątku
    app.run(debug=True, port=5000)