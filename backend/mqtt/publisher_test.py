import paho.mqtt.client as mqtt
import time

client = mqtt.Client()

client.connect("localhost", 1883)

client.loop_start()

result = client.publish(
    "durian/monitoring",
    "Halo MQTT Berhasil"
)

time.sleep(1)

client.loop_stop()

print("Data Terkirim")