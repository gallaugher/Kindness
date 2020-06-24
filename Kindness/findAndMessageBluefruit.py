"""
This is run on a Raspberry Pi and connects to a CircuitPlayground Bluefruit, sending an "A"
"""

import time
import board
import busio
import digitalio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
# from adafruit_bluefruit_connect.packet import Packet
# from adafruit_bluefruit_connect.color_packet import ColorPacket
# from adafruit_bluefruit_connect.button_packet import ButtonPacket

ble = BLERadio()

uart_connection = None

while True:
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
        ble.stop_scan()

    while uart_connection and uart_connection.connected:

        # color = (255, 254, 253)
        # print(color)
        # color_packet = ColorPacket(color)

        try:
            # uart_connection[UARTService].write(color_packet.to_bytes())

            # uart_connection[UARTService].write(ButtonPacket.UP)
            # print("I just sent an 'UP'!")
            uart_connection[UARTService].write(str.encode("A"))
            print("I just sent an 'A'!")
        except OSError:
            pass
        time.sleep(0.3)

