import paho.mqtt.client as mqtt
import sys

SERVER_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "test.mosquitto.org"
SERVER_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 1883


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def on_publish(client, userdata, result):
    print(f"data published, {result}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect(SERVER_ADDRESS)
client.subscribe("magic-mirror/face-recognition", 0)
rc = 0
while rc == 0:
    rc = client.loop()