"""
Demonstration of a Bluefruit BLE Central for Circuit Playground Bluefruit. Connects to the first BLE
UART peripheral it finds. Sends Bluefruit ColorPackets, read from three accelerometer axis, to the
peripheral.
"""

import time
import board
import busio
import digitalio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
# from adafruit_bluefruit_connect.packet import Packet
# from adafruit_bluefruit_connect.button_packet import ButtonPacket

ble = BLERadio()

uart_connection = None
# See if any existing connections are providing UARTService.
if ble.connected:
    for connection in ble.connections:
        if UARTService in connection:
            uart_connection = connection
        break

while True:
    if not uart_connection:
        print("Scanning...")
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
            print("adv.complete_name = ", adv.complete_name)
            if adv.complete_name == "BabyYoda":
                print("I found BabyYoda!")
            if UARTService in adv.services:
                print("found a UARTService advertisement")
                uart_connection = ble.connect(adv)
                print("adv.complete_name = ", adv.complete_name)
                print("ble.complete_name = ", ble.name)
                break
        # Stop scanning whether or not we are connected.
        ble.stop_scan()

    while uart_connection and uart_connection.connected:
        try:
            # uart_connection[UARTService].write(ButtonPacket.UP)
            uart_connection[UARTService].write(str.encode("A"))
            print("I just sent an 'A'!")
        except OSError:
            pass
        time.sleep(0.3)

