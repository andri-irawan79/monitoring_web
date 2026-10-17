import sys
import os
from datetime import datetime

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import json

import paho.mqtt.client as mqtt

from database.session import SessionLocal
from models.monitoring import Monitoring


def on_connect(client, userdata, flags, rc):

    print("MQTT Connected")

    client.subscribe(
        "durian/monitoring"
    )


def on_message(client, userdata, msg):

    payload = json.loads(msg.payload.decode())

    db = SessionLocal()

    data = Monitoring(
        nitrogen=payload["nitrogen"],
        phosphorus=payload["phosphorus"],
        potassium=payload["potassium"],
        temperature=payload["temperature"],
        humidity=payload["humidity"],
        ph=payload["ph"],
        rainfall=payload["rainfall"],
        simulation_date=datetime.strptime(
            payload["simulation_date"],
            "%Y-%m-%d"
        ).date()
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    print("\n" + "=" * 80)
    print("💾 DATA BERHASIL DISIMPAN KE DATABASE")
    print("=" * 80)

    print(f"ID Database  : {data.id}")
    print(f"Tanggal      : {payload['simulation_date']}")

    print("\n🌱 DATA TANAH")
    print(f"   Nitrogen   : {payload['nitrogen']} mg/kg")
    print(f"   Fosfor     : {payload['phosphorus']} mg/kg")
    print(f"   Kalium     : {payload['potassium']} mg/kg")
    print(f"   pH Tanah   : {payload['ph']:.2f}")

    print("\n🌦 DATA LINGKUNGAN")
    print(f"   Temperatur : {payload['temperature']:.2f} °C")
    print(f"   Kelembapan : {payload['humidity']:.2f} %")
    print(f"   Curah Hujan: {payload['rainfall']:.2f} mm")

    print("\n✅ Status : BERHASIL DISIMPAN")
    print("=" * 80)

    db.close()


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    "localhost",
    1883
)

client.loop_forever()