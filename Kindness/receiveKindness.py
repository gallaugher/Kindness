# BLE BELOW: Lines below setup adafruit libraries so I can send a bluetooth
# message to a CircuitPlayground Bluefruit
import busio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket

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

# BLE BELOW: Lines below setup adafruit libraries so I can send a bluetooth
# message to a CircuitPlayground Bluefruit
ble = BLERadio()
uart_connection = None

def connect_to_bluetooth_device():
    print("arrived in connect_to_bluetooth_device:")
    sending_to_CPB = True
    while sending_to_CPB:
        print("Inside while sending_to_CPB:")
        global uart_connection
        print("uart_connection = ", uart_connection)
        if not uart_connection:
            print("Scanning...")
            for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
                print("adv.complete_name = ", adv.complete_name)
                print("ble.name = ", ble.name)
                if adv.complete_name == "BabyYoda":
                    print("I found BabyYoda!")
                if UARTService in adv.services:
                    print("found a UARTService advertisement")
                    uart_connection = ble.connect(adv)
                    print("adv.complete_name = ", adv.complete_name)
                    print("ble.complete_name = ", ble.name)
                    break
            # Stop scanning whether or not we are connected.
            print("About to stop scan!")
            sending_to_CPB = False
            ble.stop_scan()

# callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with Code: " + str(rc))
    # subscribe topic
    # client.subscribe("kindness/itpcamp/")
    client.subscribe("xPra5ICM8Fh2wwcfVxiyAf2zK3D2")

def contact_via_bluetooth():
    global uart_connection
    print("I'm inside contact_via_bluetooth()!")
    print("uart_connection = ", uart_connection)
    print("uart_connection.connected = ", uart_connection.connected)
    # while uart_connection and uart_connection.connected:
    sent = False
    while uart_connection.connected and sent == False:
        print("connected!")
        color = (255, 254, 253)
        
        color_packet = ColorPacket(color)
        try:
            print("trying to send a color packet!")
            uart_connection[UARTService].write(color_packet.to_bytes())
            print("sent a color packet!")
            sending_to_CPB = False
            sent = True
        except OSError:
            print("ERROR: I couldn't send an UP")
            pass
        time.sleep(0.3)

def on_message(client, userdata, msg):
    print("received payload!", str(msg.payload))
    print(str(msg.payload))
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
    print("calling: contact_via_bluetooth()")
    contact_via_bluetooth()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.shiftr.io", 1883, 60)
client.username_pw_set("kind-one", "8e0e6b8813973531")

connect_to_bluetooth_device()

client.loop_forever()

"""
curl -X POST "http://kind-one:8e0e6b8813973531@broker.shiftr.io/kindness/itpcamp" -d "flash that light"
"""

