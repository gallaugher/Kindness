# this flashes a light attached to D18 on a Raspberry Pi
# whenever a user presses this user's name on the app.
# Be sure to change the subscribe string in line 20, below
# to the user's unique userID String in Cloud Firestore.
# receiveKindness.py
import paho.mqtt.client as mqtt
import time
import board
import digitalio

led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT

# callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with Code: " + str(rc))
    # subscribe topic
    # client.subscribe("kindness/itpcamp/")
    client.subscribe("xPra5ICM8Fh2wwcfVxiyAf2zK3D2")

def on_message(client, userdata, msg):
    print(str(msg.payload))
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.shiftr.io", 1883, 60)
client.username_pw_set("kind-one", "8e0e6b8813973531")

client.loop_forever()

"""
curl -X POST "http://kind-one:8e0e6b8813973531@broker.shiftr.io/kindness/itpcamp" -d "flash that light"
"""

