import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected!")
    client.subscribe("durian/monitoring")


def on_message(client, userdata, msg):
    print("Message:", msg.payload.decode())


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883)

client.loop_forever()