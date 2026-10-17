import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import json
import time

import paho.mqtt.client as mqtt


client = mqtt.Client()

client.connect(
    "localhost",
    1883
)

payload = {

    "nitrogen": 120,
    "phosphorus": 55,
    "potassium": 70,

    "temperature": 28,
    "humidity": 75,

    "ph": 6.8,
    "rainfall": 180
}

client.publish(
    "durian/monitoring",
    json.dumps(payload)
)

time.sleep(1)

print(
    "JSON Terkirim"
)