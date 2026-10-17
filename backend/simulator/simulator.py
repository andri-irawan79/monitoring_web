import json
import time
from datetime import datetime
from datetime import timedelta

import pandas as pd
import paho.mqtt.client as mqtt


# Lokasi dataset
DATASET_PATH = "../Crop_recommendation.csv"

# Membaca dataset
df = pd.read_csv(DATASET_PATH)

# Ambil 365 data pertama
df = df.head(365)

# MQTT Client
client = mqtt.Client()

client.connect(
    "localhost",
    1883
)

print("Simulator berjalan...")
print(f"Jumlah data: {len(df)}")

start_date = datetime(
    2026,
    1,
    1
)



for index, row in df.iterrows():

    simulation_date = (
        start_date +
        timedelta(days=index)
    ).strftime("%Y-%m-%d")

    payload = {

        "nitrogen": int(row["N"]),
        "phosphorus": int(row["P"]),
        "potassium": int(row["K"]),

        "temperature": round(float(row["temperature"]), 2),
        "humidity": round(float(row["humidity"]), 2),

        "ph": round(float(row["ph"]), 2),
        "rainfall": round(float(row["rainfall"]), 2),

        "simulation_date": simulation_date
    }

    client.publish(
        "durian/monitoring",
        json.dumps(payload)
    )

    print("=" * 70)
    print(f"Data ke-{index+1} berhasil dikirim")
    print(f"Tanggal      : {simulation_date}")
    print(f"Nitrogen     : {payload['nitrogen']} mg/kg")
    print(f"Fosfor       : {payload['phosphorus']} mg/kg")
    print(f"Kalium       : {payload['potassium']} mg/kg")
    print(f"Temperature  : {payload['temperature']} °C")
    print(f"Humidity     : {payload['humidity']} %")
    print(f"pH           : {payload['ph']}")

    print(f"Rainfall     : {payload['rainfall']} mm")

    print("=" * 70)

    time.sleep(2)